<!--
  归档管理页面组件
  功能说明：
  - 已归档发票列表展示与分页
  - 按关键字（发票号/销方/购方）搜索归档发票
  - 查看归档发票详情
  - 取消发票归档操作
-->
<template>
  <div class="archive-page">
    <el-card>
      <!-- 搜索栏：包含关键字搜索、搜索/重置按钮 -->
        <el-input
          v-model="searchForm.keyword"
          placeholder="搜索发票号/销方/购方"
          style="width: 300px"
          clearable
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" @click="handleSearch">
          <el-icon><Search /></el-icon>搜索
        </el-button>
        <el-button @click="handleReset">重置</el-button>
      </div>

      <!-- 归档发票数据表格：展示已归档发票列表，包含基本信息、归档位置、操作列 -->
      <el-table :data="tableData" style="width: 100%; margin-top: 20px" v-loading="loading">
        <el-table-column prop="invoice_number" label="发票号码" width="140" />
        <el-table-column prop="invoice_code" label="发票代码" width="140" />
        <el-table-column prop="invoice_date" label="开票日期" width="120" />
        <el-table-column prop="seller_name" label="销方名称" min-width="180" show-overflow-tooltip />
        <el-table-column prop="buyer_name" label="购方名称" min-width="180" show-overflow-tooltip />
        <el-table-column prop="total_price_tax" label="价税合计" width="120">
          <template #default="{ row }">
            ¥{{ Number(row.total_price_tax).toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="archive_location" label="归档位置" width="150" show-overflow-tooltip />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleView(row)">查看</el-button>
            <el-button link type="warning" @click="handleUnarchive(row)">取消归档</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页组件：控制当前页码、每页条数，显示总记录数 -->
      <el-pagination
        style="margin-top: 20px; justify-content: flex-end; display: flex"
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="fetchData"
        @current-change="fetchData"
      />
    </el-card>

    <!-- 发票详情对话框：以描述列表形式展示归档发票完整信息 -->
    <el-dialog v-model="detailVisible" title="发票详情" width="700px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="发票号码">{{ detailData.invoice_number }}</el-descriptions-item>
        <el-descriptions-item label="发票代码">{{ detailData.invoice_code || '-' }}</el-descriptions-item>
        <el-descriptions-item label="开票日期">{{ detailData.invoice_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="发票类型">
          {{ invoiceTypeText(detailData.invoice_type) }}
        </el-descriptions-item>
        <el-descriptions-item label="销方名称">{{ detailData.seller_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="销方税号">{{ detailData.seller_tax_no || '-' }}</el-descriptions-item>
        <el-descriptions-item label="购方名称">{{ detailData.buyer_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="购方税号">{{ detailData.buyer_tax_no || '-' }}</el-descriptions-item>
        <el-descriptions-item label="合计金额">¥{{ Number(detailData.total_amount).toFixed(2) }}</el-descriptions-item>
        <el-descriptions-item label="合计税额">¥{{ Number(detailData.total_tax).toFixed(2) }}</el-descriptions-item>
        <el-descriptions-item label="价税合计">¥{{ Number(detailData.total_price_tax).toFixed(2) }}</el-descriptions-item>
        <el-descriptions-item label="归档位置">{{ detailData.archive_location || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ detailData.remark || '-' }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
// 导入Vue组合式API
import { ref, reactive, onMounted } from 'vue'
// 导入Element Plus消息提示和确认对话框组件
import { ElMessage, ElMessageBox } from 'element-plus'
// 导入归档相关API接口函数
import { getArchiveList } from '@/api/archive'
// 导入发票相关API接口函数（重命名getInvoiceDetail为getDetail避免冲突）
import { getInvoiceDetail as getDetail, unarchiveInvoice } from '@/api/invoice'

// 表格数据加载状态
const loading = ref(false)
// 详情对话框显示状态
const detailVisible = ref(false)
// 归档发票列表数据
const tableData = ref([])
// 发票详情数据
const detailData = ref({})

// 搜索表单数据
const searchForm = reactive({
  keyword: ''  // 搜索关键字（发票号/销方/购方）
})

// 分页配置
const pagination = reactive({
  page: 1,       // 当前页码
  page_size: 10, // 每页条数
  total: 0       // 总记录数
})

// 获取归档发票列表数据
const fetchData = async () => {
  loading.value = true
  try {
    // 调用API获取归档列表，传入分页和搜索参数
    const res = await getArchiveList({
      page: pagination.page,
      page_size: pagination.page_size,
      keyword: searchForm.keyword || undefined
    })
    // 更新表格数据和总记录数
    tableData.value = res.list
    pagination.total = res.total
  } catch (error) {
    console.error('获取归档列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索处理：重置为第一页并重新获取数据
const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

// 重置搜索：清空搜索条件，重置为第一页并重新获取数据
const handleReset = () => {
  searchForm.keyword = ''
  pagination.page = 1
  fetchData()
}

// 查看归档发票详情
const handleView = async (row) => {
  try {
    const res = await getDetail(row.id)
    detailData.value = res
    detailVisible.value = true
  } catch (error) {
    console.error('获取发票详情失败:', error)
  }
}

// 取消归档：弹出确认框，确认后调用取消归档接口
const handleUnarchive = (row) => {
  ElMessageBox.confirm('确定要取消归档这张发票吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await unarchiveInvoice(row.id)
      ElMessage.success('取消归档成功')
      fetchData()
    } catch (error) {
      console.error('取消归档失败:', error)
    }
  }).catch(() => {})
}

// 发票类型文本转换：将类型数字转换为中文文本
const invoiceTypeText = (type) => {
  const map = {
    1: '增值税专用发票',
    2: '增值税普通发票',
    3: '电子专用发票',
    4: '电子普通发票'
  }
  return map[type] || '未知'
}

// 组件挂载时获取归档列表
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
/* 搜索栏样式：弹性布局，元素间距12px，垂直居中，允许换行 */
.search-bar {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}
</style>
