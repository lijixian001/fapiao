<!--
  发票管理页面组件（支持PC+移动端响应式）
  功能说明：
  - 发票列表展示与分页
  - 按关键字（发票号/销方/购方）和发票状态搜索
  - 新增、编辑、查看、删除发票
  - 发票审核、归档操作
  - 发票状态与类型的格式化显示
  - PC端：搜索栏一行多列，表格正常展示
  - 移动端：搜索栏单列垂直排列，表格横向滑动，弹窗全屏
-->
<template>
  <div class="invoice-page">
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
        <el-select
          v-model="searchForm.invoice_status"
          placeholder="发票状态"
          clearable
          class="search-item search-select"
        >
          <el-option label="待审核" :value="0" />
          <el-option label="已审核" :value="1" />
          <el-option label="已作废" :value="2" />
          <el-option label="已红冲" :value="3" />
          <el-option label="已归档" :value="4" />
          <el-option label="已抵扣" :value="5" />
        </el-select>
        <div class="search-buttons">
          <el-button type="primary" @click="handleSearch" class="search-btn">
            <el-icon><Search /></el-icon>搜索
          </el-button>
          <el-button @click="handleReset" class="search-btn">重置</el-button>
        </div>
        <el-button type="success" @click="handleAdd" class="add-btn">
          <el-icon><Plus /></el-icon>新增发票
        </el-button>
      </div>

      <!-- 发票数据表格：移动端支持横向滑动查看 -->
      <div class="table-wrapper">
        <el-table :data="tableData" v-loading="loading" class="invoice-table">
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
              <el-tag :type="statusTagType(row.invoice_status)" size="small">
                {{ statusText(row.invoice_status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="280" fixed="right">
            <template #default="{ row }">
              <el-button link type="primary" size="small" @click="handleView(row)">查看</el-button>
              <el-button link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
              <el-button v-if="row.invoice_status === 0" link type="success" size="small" @click="handleVerify(row)">
                审核
              </el-button>
              <el-button v-if="row.invoice_status !== 4" link type="warning" size="small" @click="handleArchive(row)">
                归档
              </el-button>
              <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
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

    <!-- 新增/编辑发票对话框：移动端全屏展示 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="900px"
      :fullscreen="isMobile"
      class="invoice-dialog"
      @open="handleDialogOpen"
      @close="handleDialogClose"
    >
      <el-form :model="formData" label-width="100px" class="invoice-form">
        <el-row :gutter="20">
          <el-col :span="12" :xs="24">
            <el-form-item label="发票号码">
              <el-input v-model="formData.invoice_number" />
            </el-form-item>
          </el-col>
          <el-col :span="12" :xs="24">
            <el-form-item label="发票代码">
              <el-input v-model="formData.invoice_code" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12" :xs="24">
            <el-form-item label="开票日期">
              <el-date-picker v-model="formData.invoice_date" type="date" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12" :xs="24">
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
          <el-col :span="8" :xs="24">
            <el-form-item label="合计金额">
              <el-input-number v-model="formData.total_amount" class="amount-input" :precision="2" />
            </el-form-item>
          </el-col>
          <el-col :span="8" :xs="24">
            <el-form-item label="合计税额">
              <el-input-number v-model="formData.total_tax" class="amount-input" :precision="2" />
            </el-form-item>
          </el-col>
          <el-col :span="8" :xs="24">
            <el-form-item label="价税合计">
              <el-input-number v-model="formData.total_price_tax" class="amount-input" :precision="2" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="备注">
          <el-input v-model="formData.remark" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 发票详情对话框：移动端全屏展示 -->
    <el-dialog
      v-model="detailVisible"
      title="发票详情"
      width="700px"
      :fullscreen="isMobile"
      class="detail-dialog"
    >
      <el-descriptions :column="2" border :column-mobile="1" class="detail-descriptions">
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
        <el-descriptions-item label="状态">
          <el-tag :type="statusTagType(detailData.invoice_status)" size="small">
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
import { ref, reactive, onMounted, onUnmounted } from 'vue'
// 导入Element Plus消息提示和确认对话框组件
import { ElMessage, ElMessageBox } from 'element-plus'
// 导入发票相关API接口函数
import {
  getInvoiceList,
  createInvoice,
  updateInvoice,
  deleteInvoice,
  archiveInvoice,
  verifyInvoice,
  getInvoiceDetail
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
// 是否为移动端
const isMobile = ref(false)

// 监听窗口大小变化
const handleResize = () => {
  isMobile.value = window.innerWidth <= 768
}

// 发票列表数据
const tableData = ref([])
// 发票详情数据
const detailData = ref({})

// 搜索表单数据
const searchForm = reactive({
  keyword: '',
  invoice_status: null
})

// 分页配置
const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

// 发票表单数据（新增/编辑用）
const formData = reactive({
  invoice_code: '',
  invoice_number: '',
  invoice_date: null,
  invoice_type: 1,
  seller_name: '',
  seller_tax_no: '',
  buyer_name: '',
  buyer_tax_no: '',
  total_amount: 0,
  total_tax: 0,
  total_price_tax: 0,
  remark: ''
})

// 获取发票列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const res = await getInvoiceList({
      page: pagination.page,
      page_size: pagination.page_size,
      keyword: searchForm.keyword || undefined,
      invoice_status: searchForm.invoice_status
    })
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
    const submitData = { ...formData }
    // 将空字符串金额转换为0，避免后端验证失败
    const numericFields = ['total_amount', 'total_tax', 'total_price_tax']
    numericFields.forEach(field => {
      if (submitData[field] === '' || submitData[field] === null || submitData[field] === undefined) {
        submitData[field] = 0
      }
    })
    // 将空字符串日期转换为null，避免后端验证失败
    const dateFields = ['invoice_date', 'deduct_date']
    dateFields.forEach(field => {
      if (submitData[field] === '' || submitData[field] === null || submitData[field] === undefined) {
        submitData[field] = null
      }
    })
    // 将空字符串整数字段转换为null，避免后端验证失败（仅编辑模式）
    if (isEdit.value) {
      const intFields = ['invoice_type', 'invoice_status', 'deduct_status']
      intFields.forEach(field => {
        if (submitData[field] === '' || submitData[field] === null || submitData[field] === undefined) {
          submitData[field] = null
        }
      })
    }
    if (isEdit.value) {
      await updateInvoice(editId.value, submitData)
      ElMessage.success('更新成功')
    } else {
      await createInvoice(submitData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
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

// 发票状态文本转换
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

// 发票状态标签类型转换
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

// 对话框打开时处理（移动端键盘适配）
const handleDialogOpen = () => {
  if (isMobile.value) {
    document.body.style.overflow = 'hidden'
    window.addEventListener('resize', handleDialogResize)
  }
}

// 对话框关闭时处理（移除键盘适配）
const handleDialogClose = () => {
  if (isMobile.value) {
    document.body.style.overflow = ''
    window.removeEventListener('resize', handleDialogResize)
  }
}

// 对话框键盘弹出时的滚动处理
const handleDialogResize = () => {
  if (isMobile.value && dialogVisible.value) {
    setTimeout(() => {
      const activeElement = document.activeElement
      if (activeElement) {
        activeElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    }, 100)
  }
}
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

.search-select {
  width: 150px;
}

.search-buttons {
  display: flex;
  gap: 8px;
}

.add-btn {
  margin-left: auto;
}

/* ========== 表格样式 ========== */
.table-wrapper {
  margin-top: 20px;
  width: 100%;
  overflow-x: auto;
}

.invoice-table {
  width: 100%;
  min-width: 800px;
}

/* ========== 分页样式 ========== */
.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* ========== 对话框底部按钮 ========== */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* ========== 表单详情描述 ========== */
.detail-descriptions {
  width: 100%;
}

/* ========== 金额输入框样式 ========== */
.amount-input {
  width: 100%;
  min-width: 150px;
}

.amount-input :deep(.el-input-number) {
  width: 100%;
}

.amount-input :deep(.el-input-number__input) {
  text-align: right;
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
  padding-right: 30px;
}

.amount-input :deep(.el-input-number__increase),
.amount-input :deep(.el-input-number__decrease) {
  padding: 0 8px;
}

/* ========== 移动端对话框样式 ========== */
.invoice-dialog :deep(.el-dialog__body) {
  max-height: calc(100vh - 140px);
  overflow-y: auto;
}

.invoice-dialog :deep(.el-dialog) {
  max-height: 100vh;
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

  .add-btn {
    margin-left: 0;
    width: 100%;
    min-height: 44px;
  }

  /* 表格区域调整 */
  .table-wrapper {
    margin-top: 15px;
    margin-left: -12px;
    margin-right: -12px;
    width: calc(100% + 24px);
  }

  .invoice-table {
    font-size: 13px;
  }

  /* 分页居中 */
  .pagination-wrapper {
    justify-content: center;
    margin-top: 15px;
    overflow-x: auto;
  }

  /* 表单标签宽度调整 */
  .invoice-form :deep(.el-form-item__label) {
    width: 80px !important;
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
