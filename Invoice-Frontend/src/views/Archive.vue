<!--
  归档管理页面组件（支持PC+移动端响应式）
  功能说明：
  - 已归档发票列表展示与分页
  - 按关键字（发票号/销方/购方）搜索归档发票
  - 查看归档发票详情
  - 取消发票归档操作
  - PC端：搜索栏一行多列，表格正常展示
  - 移动端：搜索栏单列垂直排列，表格横向滑动，弹窗全屏
-->
<template>
  <div class="archive-page">
    <el-card class="page-card">
      <!-- 搜索栏：PC端一行多列，移动端单列垂直排列 -->
      <div class="search-bar">
        <el-input
          v-model="searchForm.keyword"
          placeholder="搜索发票号/销方/购方"
          clearable
          @keyup.enter="handleSearch"
          class="search-item search-input"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <div class="search-buttons">
          <el-button type="primary" @click="handleSearch" class="search-btn">
            <el-icon><Search /></el-icon>搜索
          </el-button>
          <el-button @click="handleReset" class="search-btn">重置</el-button>
        </div>
      </div>

      <!-- 归档发票数据表格：移动端支持横向滑动查看 -->
      <div class="table-wrapper">
        <el-table :data="tableData" v-loading="loading" class="archive-table">
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
              <el-button link type="primary" size="small" @click="handleView(row)">查看</el-button>
              <el-button link type="warning" size="small" @click="handleUnarchive(row)">取消归档</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 分页组件：移动端居中对齐 -->
      <el-pagination
        class="pagination-wrapper"
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="fetchData"
        @current-change="fetchData"
      />
    </el-card>

    <!-- 发票详情对话框：移动端全屏展示 -->
    <el-dialog
      v-model="detailVisible"
      title="发票详情"
      width="700px"
      :fullscreen="isMobile"
      class="detail-dialog"
    >
      <el-descriptions :column="2" border class="detail-descriptions">
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
        <el-descriptions-item label="合计金额">¥{{ Number(detailData.total_amount || 0).toFixed(2) }}</el-descriptions-item>
        <el-descriptions-item label="合计税额">¥{{ Number(detailData.total_tax || 0).toFixed(2) }}</el-descriptions-item>
        <el-descriptions-item label="价税合计">¥{{ Number(detailData.total_price_tax || 0).toFixed(2) }}</el-descriptions-item>
        <el-descriptions-item label="归档位置">{{ detailData.archive_location || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ detailData.remark || '-' }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
// 导入Vue组合式API
import { ref, reactive, onMounted, onUnmounted } from 'vue'
// 导入Element Plus消息提示和确认对话框组件
import { ElMessage, ElMessageBox } from 'element-plus'
// 导入归档相关API接口函数
import { getArchiveList } from '@/api/archive'
// 导入发票相关API接口函数
import { getInvoiceDetail as getDetail, unarchiveInvoice } from '@/api/invoice'

// 表格数据加载状态
const loading = ref(false)
// 详情对话框显示状态
const detailVisible = ref(false)
// 是否为移动端
const isMobile = ref(false)

// 监听窗口大小变化
const handleResize = () => {
  isMobile.value = window.innerWidth <= 768
}

// 归档发票列表数据
const tableData = ref([])
// 发票详情数据
const detailData = ref({})

// 搜索表单数据
const searchForm = reactive({
  keyword: ''
})

// 分页配置
const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

// 获取归档发票列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const res = await getArchiveList({
      page: pagination.page,
      page_size: pagination.page_size,
      keyword: searchForm.keyword || undefined
    })
    tableData.value = res.list
    pagination.total = res.total
  } catch (error) {
    console.error('获取归档列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

// 重置搜索
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

// 取消归档
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

// 发票类型文本转换
const invoiceTypeText = (type) => {
  const map = {
    1: '增值税专用发票',
    2: '增值税普通发票',
    3: '电子专用发票',
    4: '电子普通发票'
  }
  return map[type] || '未知'
}

// 组件挂载时
onMounted(() => {
  handleResize()
  window.addEventListener('resize', handleResize)
  fetchData()
})

// 组件卸载时
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
/* 页面卡片容器 */
.page-card {
  width: 100%;
}

/* ========== 搜索栏样式 ========== */
.search-bar {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.search-item {
  flex-shrink: 0;
}

.search-input {
  width: 300px;
}

.search-buttons {
  display: flex;
  gap: 8px;
}

/* ========== 表格样式 ========== */
.table-wrapper {
  margin-top: 20px;
  width: 100%;
  overflow-x: auto;
}

.archive-table {
  width: 100%;
  min-width: 800px;
}

/* ========== 分页样式 ========== */
.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* ========== 表单详情描述 ========== */
.detail-descriptions {
  width: 100%;
}

/* ========== 移动端响应式样式（<=768px） ========== */
@media screen and (max-width: 768px) {
  /* 搜索栏改为垂直排列 */
  .search-bar {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }

  .search-item {
    width: 100% !important;
  }

  .search-buttons {
    width: 100%;
    display: flex;
    gap: 10px;
  }

  .search-btn {
    flex: 1;
    min-height: 44px;
  }

  /* 表格区域调整 */
  .table-wrapper {
    margin-top: 15px;
    margin-left: -12px;
    margin-right: -12px;
    width: calc(100% + 24px);
  }

  .archive-table {
    font-size: 13px;
  }

  /* 分页居中 */
  .pagination-wrapper {
    justify-content: center;
    margin-top: 15px;
    overflow-x: auto;
  }
}

/* ========== 小屏幕适配（<=480px） ========== */
@media screen and (max-width: 480px) {
  .table-wrapper {
    margin-left: -10px;
    margin-right: -10px;
    width: calc(100% + 20px);
  }
}
</style>
