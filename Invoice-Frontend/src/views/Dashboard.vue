<!--
  组件名称：Dashboard.vue
  组件用途：系统仪表盘页面
  功能说明：
    - 展示发票管理系统的核心统计数据（发票总数、已审核、待处理、已归档）
    - 以卡片形式展示统计指标，不同状态用不同颜色区分
    - 提供欢迎信息和系统功能介绍
    - 提供快速入口（录入发票、审核发票、归档管理）
    - 页面加载时从后端获取统计数据
-->
<template>
  <!-- 仪表盘页面容器 -->
  <div class="dashboard">
    <!-- 统计卡片行 - 四个统计卡片，间距20px -->
    <el-row :gutter="20">
      <!-- 发票总数统计卡片 - 占6列（共24列） -->
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <!-- 统计图标 - 蓝色背景 -->
            <div class="stat-icon" style="background: #409EFF">
              <el-icon :size="30"><Document /></el-icon>
            </div>
            <!-- 统计信息 - 数值和标签 -->
            <div class="stat-info">
              <div class="stat-value">{{ stats.total }}</div>
              <div class="stat-label">发票总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <!-- 已审核发票统计卡片 - 占6列 -->
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <!-- 统计图标 - 绿色背景 -->
            <div class="stat-icon" style="background: #67C23A">
              <el-icon :size="30"><CircleCheck /></el-icon>
            </div>
            <!-- 统计信息 - 数值和标签 -->
            <div class="stat-info">
              <div class="stat-value">{{ stats.verified }}</div>
              <div class="stat-label">已审核</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <!-- 待处理发票统计卡片 - 占6列 -->
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <!-- 统计图标 - 橙色背景 -->
            <div class="stat-icon" style="background: #E6A23C">
              <el-icon :size="30"><Clock /></el-icon>
            </div>
            <!-- 统计信息 - 数值和标签 -->
            <div class="stat-info">
              <div class="stat-value">{{ stats.pending }}</div>
              <div class="stat-label">待处理</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <!-- 已归档发票统计卡片 - 占6列 -->
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <!-- 统计图标 - 灰色背景 -->
            <div class="stat-icon" style="background: #909399">
              <el-icon :size="30"><Folder /></el-icon>
            </div>
            <!-- 统计信息 - 数值和标签 -->
            <div class="stat-info">
              <div class="stat-value">{{ stats.archived }}</div>
              <div class="stat-label">已归档</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 欢迎卡片 - 包含系统介绍和快速入口 -->
    <el-card class="welcome-card" style="margin-top: 20px">
      <h2>欢迎使用企业发票管理业务系统</h2>
      <p>这是一个功能完善的发票管理系统，支持发票录入、审核、归档、抵扣等全流程管理。</p>
      <!-- 分隔线 -->
      <el-divider />
      <h3>快速开始</h3>
      <!-- 快速入口行 - 三个快速操作项 -->
      <el-row :gutter="20">
        <!-- 录入发票快速入口 - 占8列 -->
        <el-col :span="8">
          <div class="quick-item" @click="$router.push('/invoice')">
            <el-icon :size="24" style="color: #409EFF"><Plus /></el-icon>
            <span>录入发票</span>
          </div>
        </el-col>
        <!-- 审核发票快速入口 - 占8列 -->
        <el-col :span="8">
          <div class="quick-item" @click="$router.push('/invoice')">
            <el-icon :size="24" style="color: #67C23A"><CircleCheck /></el-icon>
            <span>审核发票</span>
          </div>
        </el-col>
        <!-- 归档管理快速入口 - 占8列 -->
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
// 导入Vue组合式API - ref定义响应式数据，onMounted生命周期钩子
import { ref, onMounted } from 'vue'
// 导入发票列表API接口
import { getInvoiceList } from '@/api/invoice'

// 统计数据 - 包含发票总数、已审核、待处理、已归档四个指标
const stats = ref({
  total: 0,
  verified: 0,
  pending: 0,
  archived: 0
})

/**
 * 组件挂载生命周期钩子
 * 功能：页面加载时获取各类发票的统计数据
 * 说明：通过调用发票列表接口，传入不同的状态参数来获取各状态的发票总数
 */
onMounted(async () => {
  try {
    // 获取全部发票总数（不传状态参数）
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
    // 打印获取统计数据失败的错误信息
    console.error('获取统计数据失败:', error)
  }
})
</script>

<style scoped>
/* 统计卡片样式 - 圆角效果 */
.stat-card {
  border-radius: 8px;
}

/* 统计内容布局 - 水平排列，图标和信息并排 */
.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* 统计图标样式 - 圆角正方形，居中显示图标，白色图标 */
.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

/* 统计数值样式 - 大字号，加粗 */
.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

/* 统计标签样式 - 小字号，灰色 */
.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

/* 欢迎卡片样式 - 圆角效果 */
.welcome-card {
  border-radius: 8px;
}

/* 欢迎卡片主标题样式 */
.welcome-card h2 {
  color: #303133;
  margin-bottom: 8px;
}

/* 欢迎卡片副标题样式 */
.welcome-card h3 {
  color: #606266;
  margin-bottom: 16px;
}

/* 欢迎卡片描述文字样式 */
.welcome-card p {
  color: #909399;
}

/* 快速入口项样式 - 垂直排列，居中，背景浅灰，可点击，悬停有动画效果 */
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

/* 快速入口项悬停效果 - 背景变深，轻微上移 */
.quick-item:hover {
  background: #e9eef5;
  transform: translateY(-2px);
}
</style>
