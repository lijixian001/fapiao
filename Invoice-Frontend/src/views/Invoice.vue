<!--
  发票管理页面组件
  功能说明：
  - 发票列表展示与分页
  - 按关键字（发票号/销方/购方）和发票状态搜索
  - 新增、编辑、查看、删除发票
  - 发票审核、归档操作
  - 发票状态与类型的格式化显示
-->
<template>
  <div class="invoice-page">
    <el-card>
      <!-- 搜索栏：包含关键字搜索、状态筛选、搜索/重置按钮、新增按钮 -->
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
        <el-select v-model="searchForm.invoice_status" placeholder="发票状态" style="width: 150px" clearable>
          <el-option label="待审核" :value="0" />
          <el-option label="已审核" :value="1" />
          <el-option label="已作废" :value="2" />
          <el-option label="已红冲" :value="3" />
          <el-option label="已归档" :value="4" />
          <el-option label="已抵扣" :value="5" />
        </el-select>
        <el-button type="primary" @click="handleSearch">
          <el-icon><Search /></el-icon>搜索
        </el-button>
        <el-button @click="handleReset">重置</el-button>
        <el-button type="success" style="margin-left: auto" @click="handleAdd">
          <el-icon><Plus /></el-icon>新增发票
        </el-button>
      </div>

      <!-- 发票数据表格：展示发票列表，包含发票基本信息、状态、操作列 -->
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
        <el-table-column prop="invoice_status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.invoice_status)">
              {{ statusText(row.invoice_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleView(row)">查看</el-button>
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="row.invoice_status === 0" link type="success" @click="handleVerify(row)">
              审核
            </el-button>
            <el-button v-if="row.invoice_status !== 4" link type="warning" @click="handleArchive(row)">
              归档
            </el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
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

    <!-- 新增/编辑发票对话框：包含发票完整信息表单 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="700px">
      <el-form :model="formData" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="发票代码">
              <el-input v-model="formData.invoice_code" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="发票号码">
              <el-input v-model="formData.invoice_number" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="开票日期">
              <el-date-picker v-model="formData.invoice_date" type="date" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="发票类型">
              <el-select v-model="formData.invoice_type" style="width: 100%">
                <el-option label="增值税专用发票" :value="1" />
                <el-option label="增值税普通发票" :value="2" />
                <el-option label="电子专用发票" :value="3" />
                <el-option label="电子普通发票" :value="4" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="销方名称">
          <el-input v-model="formData.seller_name" />
        </el-form-item>
        <el-form-item label="销方税号">
          <el-input v-model="formData.seller_tax_no" />
        </el-form-item>
        <el-form-item label="购方名称">
          <el-input v-model="formData.buyer_name" />
        </el-form-item>
        <el-form-item label="购方税号">
          <el-input v-model="formData.buyer_tax_no" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="合计金额">
              <el-input-number v-model="formData.total_amount" style="width: 100%" :precision="2" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="合计税额">
              <el-input-number v-model="formData.total_tax" style="width: 100%" :precision="2" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="价税合计">
              <el-input-number v-model="formData.total_price_tax" style="width: 100%" :precision="2" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="备注">
          <el-input v-model="formData.remark" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>

    <!-- 发票详情对话框：以描述列表形式展示发票完整信息 -->
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
        <el-descriptions-item label="状态">
          <el-tag :type="statusTagType(detailData.invoice_status)">
            {{ statusText(detailData.invoice_status) }}
          </el-tag>
        </el-descriptions-item>
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
// 导入发票相关API接口函数
import {
  getInvoiceList,    // 获取发票列表
  createInvoice,     // 创建发票
  updateInvoice,     // 更新发票
  deleteInvoice,     // 删除发票
  archiveInvoice,    // 归档发票
  verifyInvoice,     // 审核发票
  getInvoiceDetail   // 获取发票详情
} from '@/api/invoice'

// 表格数据加载状态
const loading = ref(false)
// 表单提交加载状态
const submitLoading = ref(false)
// 新增/编辑对话框显示状态
const dialogVisible = ref(false)
// 详情对话框显示状态
const detailVisible = ref(false)
// 对话框标题
const dialogTitle = ref('')
// 是否为编辑模式
const isEdit = ref(false)
// 当前编辑的发票ID
const editId = ref(null)

// 发票列表数据
const tableData = ref([])
// 发票详情数据
const detailData = ref({})

// 搜索表单数据
const searchForm = reactive({
  keyword: '',          // 搜索关键字（发票号/销方/购方）
  invoice_status: null  // 发票状态筛选
})

// 分页配置
const pagination = reactive({
  page: 1,       // 当前页码
  page_size: 10, // 每页条数
  total: 0       // 总记录数
})

// 发票表单数据（新增/编辑用）
const formData = reactive({
  invoice_code: '',      // 发票代码
  invoice_number: '',    // 发票号码
  invoice_date: null,    // 开票日期
  invoice_type: 1,       // 发票类型（1：专票，2：普票，3：电子专票，4：电子普票）
  seller_name: '',       // 销方名称
  seller_tax_no: '',     // 销方税号
  buyer_name: '',        // 购方名称
  buyer_tax_no: '',      // 购方税号
  total_amount: 0,       // 合计金额
  total_tax: 0,          // 合计税额
  total_price_tax: 0,    // 价税合计
  remark: ''             // 备注
})

// 获取发票列表数据
const fetchData = async () => {
  loading.value = true
  try {
    // 调用API获取发票列表，传入分页和搜索参数
    const res = await getInvoiceList({
      page: pagination.page,
      page_size: pagination.page_size,
      keyword: searchForm.keyword || undefined,
      invoice_status: searchForm.invoice_status
    })
    // 更新表格数据和总记录数
    tableData.value = res.list
    pagination.total = res.total
  } catch (error) {
    console.error('获取发票列表失败:', error)
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
  searchForm.invoice_status = null
  pagination.page = 1
  fetchData()
}

// 新增发票：打开新增对话框，重置表单数据
const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = '新增发票'
  editId.value = null
  // 重置表单数据，根据字段类型设置默认值
  Object.keys(formData).forEach(key => {
    if (key === 'invoice_type') {
      formData[key] = 1
    } else if (['total_amount', 'total_tax', 'total_price_tax'].includes(key)) {
      formData[key] = 0
    } else {
      formData[key] = ''
    }
  })
  formData.invoice_date = null
  dialogVisible.value = true
}

// 编辑发票：打开编辑对话框，填充当前行数据
const handleEdit = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑发票'
  editId.value = row.id
  // 将当前行数据合并到表单中
  Object.assign(formData, row)
  dialogVisible.value = true
}

// 查看发票详情
const handleView = async (row) => {
  try {
    const res = await getInvoiceDetail(row.id)
    detailData.value = res
    detailVisible.value = true
  } catch (error) {
    console.error('获取发票详情失败:', error)
  }
}

// 提交表单：根据isEdit判断是新增还是编辑
const handleSubmit = async () => {
  try {
    submitLoading.value = true
    if (isEdit.value) {
      // 编辑模式：调用更新接口
      await updateInvoice(editId.value, formData)
      ElMessage.success('更新成功')
    } else {
      // 新增模式：调用创建接口
      await createInvoice(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    // 刷新列表数据
    fetchData()
  } catch (error) {
    console.error('提交失败:', error)
  } finally {
    submitLoading.value = false
  }
}

// 删除发票：弹出确认框，确认后调用删除接口
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除这张发票吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteInvoice(row.id)
      ElMessage.success('删除成功')
      fetchData()
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

// 审核发票：弹出确认框，确认后调用审核接口
const handleVerify = (row) => {
  ElMessageBox.confirm('确定要审核这张发票吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'success'
  }).then(async () => {
    try {
      await verifyInvoice(row.id)
      ElMessage.success('审核成功')
      fetchData()
    } catch (error) {
      console.error('审核失败:', error)
    }
  }).catch(() => {})
}

// 归档发票：弹出确认框，确认后调用归档接口
const handleArchive = (row) => {
  ElMessageBox.confirm('确定要归档这张发票吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await archiveInvoice(row.id)
      ElMessage.success('归档成功')
      fetchData()
    } catch (error) {
      console.error('归档失败:', error)
    }
  }).catch(() => {})
}

// 发票状态文本转换：将状态数字转换为中文文本
const statusText = (status) => {
  const map = {
    0: '待审核',
    1: '已审核',
    2: '已作废',
    3: '已红冲',
    4: '已归档',
    5: '已抵扣'
  }
  return map[status] || '未知'
}

// 发票状态标签类型转换：根据状态返回对应的Element Plus标签类型
const statusTagType = (status) => {
  const map = {
    0: 'warning',
    1: 'success',
    2: 'info',
    3: 'danger',
    4: '',
    5: 'success'
  }
  return map[status] || 'info'
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

// 组件挂载时获取发票列表
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
