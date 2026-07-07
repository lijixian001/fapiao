<!--
  组件名称：Dashboard.vue
  组件用途：系统仪表盘页面（支持PC+移动端响应式）
  功能说明：
    - 展示发票管理系统的核心统计数据（发票总数、已审核、待处理、已归档）
    - 以卡片形式展示统计指标，不同状态用不同颜色区分
    - 提供欢迎信息和系统功能介绍
    - 提供快速入口（录入发票、审核发票、归档管理）
    - 页面加载时从后端获取统计数据
    - PC端：四列统计卡片，三列快速入口
    - 移动端：两列统计卡片，单列快速入口
-->
<template>
  <!-- 仪表盘页面容器 -->
  <div class="dashboard">
    <!-- 统计卡片行 -->
    <el-row :gutter="16" class="stat-row">
      <!-- 发票总数统计卡片 -->
      <el-col :xs="12" :sm="12" :md="6" :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #409EFF">
              <el-icon :size="26"><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total }}</div>
              <div class="stat-label">发票总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <!-- 已审核发票统计卡片 -->
      <el-col :xs="12" :sm="12" :md="6" :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #67C23A">
              <el-icon :size="26"><CircleCheck /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.verified }}</div>
              <div class="stat-label">已审核</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <!-- 待处理发票统计卡片 -->
      <el-col :xs="12" :sm="12" :md="6" :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #E6A23C">
              <el-icon :size="26"><Clock /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.pending }}</div>
              <div class="stat-label">待处理</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <!-- 已归档发票统计卡片 -->
      <el-col :xs="12" :sm="12" :md="6" :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #909399">
              <el-icon :size="26"><Folder /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.archived }}</div>
              <div class="stat-label">已归档</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 欢迎卡片 -->
    <el-card class="welcome-card">
      <h2>欢迎使用企业发票管理业务系统</h2>
      <p>这是一个功能完善的发票管理系统，支持发票录入、审核、归档、抵扣等全流程管理。</p>
      <el-divider />
      <h3>快速开始</h3>
      <!-- 快速入口行 -->
      <el-row :gutter="16">
        <el-col :xs="24" :sm="8" :span="8">
          <div class="quick-item" @click="$router.push('/invoice')">
            <el-icon :size="24" style="color: #409EFF"><Plus /></el-icon>
            <span>录入发票</span>
          </div>
        </el-col>
        <el-col :xs="24" :sm="8" :span="8">
          <div class="quick-item" @click="$router.push('/invoice')">
            <el-icon :size="24" style="color: #67C23A"><CircleCheck /></el-icon>
            <span>审核发票</span>
          </div>
        </el-col>
        <el-col :xs="24" :sm="8" :span="8">
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
// 导入Vue组合式API
import { ref, onMounted } from 'vue'
// 导入发票列表API接口
import { getInvoiceList } from '@/api/invoice'

// 统计数据
const stats = ref({
  total: 0,
  verified: 0,
  pending: 0,
  archived: 0
})

/**
 * 组件挂载生命周期钩子
 * 功能：页面加载时获取各类发票的统计数据
 */
onMounted(async () => {
  try {
    // 获取全部发票总数
    const allRes = await getInvoiceList({ page: 1, page_size: 1 })
    stats.value.total = allRes.total

    // 获取待处理发票总数（状态0）
    const pendingRes = await getInvoiceList({ page: 1, page_size: 1, invoice_status: 0 })
    stats.value.pending = pendingRes.total

    // 获取已审核发票总数（状态1）
    const verifiedRes = await getInvoiceList({ page: 1, page_size: 1, invoice_status: 1 })
    stats.value.verified = verifiedRes.total

    // 获取已归档发票总数（状态4）
    const archivedRes = await getInvoiceList({ page: 1, page_size: 1, invoice_status: 4 })
    stats.value.archived = archivedRes.total
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
})
</script>

<style scoped>
/* 统计卡片行间距 */
.stat-row {
  margin-bottom: 0;
}

/* 统计卡片样式 */
.stat-card {
  border-radius: 8px;
  margin-bottom: 16px;
}

/* 统计内容布局 */
.stat-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 统计图标样式 */
.stat-icon {
  width: 52px;
  height: 52px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
}

/* 统计数值样式 */
.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  line-height: 1.2;
}

/* 统计标签样式 */
.stat-label {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}

/* 欢迎卡片样式 */
.welcome-card {
  border-radius: 8px;
  margin-top: 4px;
}

/* 欢迎卡片主标题样式 */
.welcome-card h2 {
  color: #303133;
  margin-bottom: 8px;
  font-size: 20px;
}

/* 欢迎卡片副标题样式 */
.welcome-card h3 {
  color: #606266;
  margin-bottom: 16px;
  font-size: 16px;
}

/* 欢迎卡片描述文字样式 */
.welcome-card p {
  color: #909399;
  font-size: 14px;
}

/* 快速入口项样式 */
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
  margin-bottom: 16px;
}

/* 快速入口项悬停效果 */
.quick-item:hover {
  background: #e9eef5;
  transform: translateY(-2px);
}

/* ========== 移动端响应式样式（<=768px） ========== */
@media screen and (max-width: 768px) {
  .stat-card {
    margin-bottom: 12px;
  }

  .stat-content {
    gap: 10px;
  }

  .stat-icon {
    width: 46px;
    height: 46px;
    border-radius: 8px;
  }

  .stat-value {
    font-size: 20px;
  }

  .stat-label {
    font-size: 12px;
  }

  .welcome-card {
    margin-top: 0;
  }

  .welcome-card h2 {
    font-size: 18px;
  }

  .welcome-card h3 {
    font-size: 15px;
  }

  .quick-item {
    padding: 16px;
    margin-bottom: 12px;
    min-height: 80px;
  }
}

/* ========== 小屏幕适配（<=480px） ========== */
@media screen and (max-width: 480px) {
  .stat-value {
    font-size: 18px;
  }

  .stat-icon {
    width: 42px;
    height: 42px;
  }

  .quick-item {
    padding: 14px;
    min-height: 72px;
  }
}
</style>
