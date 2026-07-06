<template>
  <div class="archive-page">
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
        <el-button type="primary" @click="handleSearch">
          <el-icon><Search /></el-icon>搜索
        </el-button>
        <el-button @click="handleReset">重置</el-button>
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
        <el-table-column prop="archive_location" label="归档位置" width="150" show-overflow-tooltip />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleView(row)">查看</el-button>
            <el-button link type="warning" @click="handleUnarchive(row)">取消归档</el-button>
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getArchiveList } from '@/api/archive'
import { getInvoiceDetail as getDetail, unarchiveInvoice } from '@/api/invoice'

const loading = ref(false)
const detailVisible = ref(false)
const tableData = ref([])
const detailData = ref({})

const searchForm = reactive({
  keyword: ''
})

const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

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

const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

const handleReset = () => {
  searchForm.keyword = ''
  pagination.page = 1
  fetchData()
}

const handleView = async (row) => {
  try {
    const res = await getDetail(row.id)
    detailData.value = res
    detailVisible.value = true
  } catch (error) {
    console.error('获取发票详情失败:', error)
  }
}

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
