<template>
  <div class="invoice-page">
    <el-card>
      <div class="search-bar">
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getInvoiceList,
  createInvoice,
  updateInvoice,
  deleteInvoice,
  archiveInvoice,
  verifyInvoice,
  getInvoiceDetail
} from '@/api/invoice'

const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const editId = ref(null)

const tableData = ref([])
const detailData = ref({})

const searchForm = reactive({
  keyword: '',
  invoice_status: null
})

const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

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

const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

const handleReset = () => {
  searchForm.keyword = ''
  searchForm.invoice_status = null
  pagination.page = 1
  fetchData()
}

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

const handleEdit = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑发票'
  editId.value = row.id
  Object.assign(formData, row)
  dialogVisible.value = true
}

const handleView = async (row) => {
  try {
    const res = await getInvoiceDetail(row.id)
    detailData.value = res
    detailVisible.value = true
  } catch (error) {
    console.error('获取发票详情失败:', error)
  }
}

const handleSubmit = async () => {
  try {
    submitLoading.value = true
    if (isEdit.value) {
      await updateInvoice(editId.value, formData)
      ElMessage.success('更新成功')
    } else {
      await createInvoice(formData)
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

const invoiceTypeText = (type) => {
  const map = {
    1: '增值税专用发票',
    2: '增值税普通发票',
    3: '电子专用发票',
    4: '电子普通发票'
  }
  return map[type] || '未知'
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}
</style>
