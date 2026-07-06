<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #409EFF">
              <el-icon :size="30"><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total }}</div>
              <div class="stat-label">发票总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #67C23A">
              <el-icon :size="30"><CircleCheck /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.verified }}</div>
              <div class="stat-label">已审核</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #E6A23C">
              <el-icon :size="30"><Clock /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.pending }}</div>
              <div class="stat-label">待处理</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #909399">
              <el-icon :size="30"><Folder /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.archived }}</div>
              <div class="stat-label">已归档</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="welcome-card" style="margin-top: 20px">
      <h2>欢迎使用企业发票管理业务系统</h2>
      <p>这是一个功能完善的发票管理系统，支持发票录入、审核、归档、抵扣等全流程管理。</p>
      <el-divider />
      <h3>快速开始</h3>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="quick-item" @click="$router.push('/invoice')">
            <el-icon :size="24" style="color: #409EFF"><Plus /></el-icon>
            <span>录入发票</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="quick-item" @click="$router.push('/invoice')">
            <el-icon :size="24" style="color: #67C23A"><CircleCheck /></el-icon>
            <span>审核发票</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="quick-item" @click="$router.push('/archive')">
            <el-icon :size="24" style="color: #909399"><Folder /></el-icon>
            <span>归档管理</span>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getInvoiceList } from '@/api/invoice'

const stats = ref({
  total: 0,
  verified: 0,
  pending: 0,
  archived: 0
})

onMounted(async () => {
  try {
    const allRes = await getInvoiceList({ page: 1, page_size: 1 })
    stats.value.total = allRes.total

    const pendingRes = await getInvoiceList({ page: 1, page_size: 1, invoice_status: 0 })
    stats.value.pending = pendingRes.total

    const verifiedRes = await getInvoiceList({ page: 1, page_size: 1, invoice_status: 1 })
    stats.value.verified = verifiedRes.total

    const archivedRes = await getInvoiceList({ page: 1, page_size: 1, invoice_status: 4 })
    stats.value.archived = archivedRes.total
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
})
</script>

<style scoped>
.stat-card {
  border-radius: 8px;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.welcome-card {
  border-radius: 8px;
}

.welcome-card h2 {
  color: #303133;
  margin-bottom: 8px;
}

.welcome-card h3 {
  color: #606266;
  margin-bottom: 16px;
}

.welcome-card p {
  color: #909399;
}

.quick-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  gap: 8px;
}

.quick-item:hover {
  background: #e9eef5;
  transform: translateY(-2px);
}
</style>
