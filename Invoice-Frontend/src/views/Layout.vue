<!--
  组件名称：Layout.vue
  组件用途：系统主布局组件
  功能说明：
    - 提供系统整体布局结构（侧边栏 + 头部 + 主内容区）
    - 左侧导航菜单，支持页面切换
    - 顶部头部显示当前页面标题和用户信息
    - 用户下拉菜单（个人信息、退出登录）
    - 主内容区通过router-view渲染子页面
-->
<template>
  <!-- 整体布局容器 - 使用Element Plus的Container布局组件 -->
  <el-container class="layout-container">
    <!-- 左侧侧边栏 - 宽度220px -->
    <el-aside width="220px" class="layout-aside">
      <!-- Logo区域 -->
      <div class="logo">
        <el-icon :size="28"><Document /></el-icon>
        <span>发票管理系统</span>
      </div>
      <!-- 左侧导航菜单 - 深色主题 -->
      <el-menu
        :default-active="activeMenu"
        class="layout-menu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        @select="handleMenuSelect"
      >
        <!-- 仪表盘菜单项 -->
        <el-menu-item index="/dashboard">
          <el-icon><HomeFilled /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <!-- 发票管理菜单项 -->
        <el-menu-item index="/invoice">
          <el-icon><Document /></el-icon>
          <span>发票管理</span>
        </el-menu-item>
        <!-- 归档管理菜单项 -->
        <el-menu-item index="/archive">
          <el-icon><Folder /></el-icon>
          <span>归档管理</span>
        </el-menu-item>
        <!-- 用户管理菜单项 -->
        <el-menu-item index="/user">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <!-- 右侧主容器 - 包含头部和主内容区 -->
    <el-container>
      <!-- 顶部头部栏 -->
      <el-header class="layout-header">
        <!-- 头部左侧 - 显示当前页面标题 -->
        <div class="header-left">
          <span class="page-title">{{ pageTitle }}</span>
        </div>
        <!-- 头部右侧 - 用户信息下拉菜单 -->
        <div class="header-right">
          <!-- 用户下拉菜单 -->
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-icon><UserFilled /></el-icon>
              {{ userInfo.real_name }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <!-- 下拉菜单内容 -->
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <!-- 主内容区域 - 通过router-view渲染子页面 -->
      <el-main class="layout-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
// 导入Vue组合式API - ref定义响应式数据，computed计算属性，onMounted生命周期钩子
import { ref, computed, onMounted } from 'vue'
// 导入Vue路由 - useRoute获取当前路由信息，useRouter进行路由跳转
import { useRoute, useRouter } from 'vue-router'
// 导入Element Plus组件 - ElMessage消息提示，ElMessageBox确认对话框
import { ElMessage, ElMessageBox } from 'element-plus'
// 导入退出登录API接口
import { logout } from '@/api/auth'

// 获取当前路由对象
const route = useRoute()
// 获取路由实例
const router = useRouter()

// 用户信息 - 存储当前登录用户的用户名和真实姓名
const userInfo = ref({
  username: '',
  real_name: ''
})

// 计算属性：当前激活的菜单项 - 根据当前路由路径自动高亮对应的菜单项
const activeMenu = computed(() => route.path)

// 计算属性：当前页面标题 - 根据路由路径映射对应的中文标题
const pageTitle = computed(() => {
  // 路由路径与页面标题的映射表
  const titles = {
    '/dashboard': '仪表盘',
    '/invoice': '发票管理',
    '/archive': '归档管理',
    '/user': '用户管理'
  }
  // 返回对应标题，默认显示'仪表盘'
  return titles[route.path] || '仪表盘'
})

/**
 * 组件挂载生命周期钩子
 * 功能：从本地存储中读取用户信息并赋值
 */
onMounted(() => {
  // 从localStorage获取用户信息
  const info = localStorage.getItem('userInfo')
  // 如果存在用户信息，则解析并赋值
  if (info) {
    userInfo.value = JSON.parse(info)
  }
})

/**
 * 菜单选择处理函数
 * @param {string} index - 菜单项的索引（路由路径）
 * 功能：点击菜单项时跳转到对应页面
 */
const handleMenuSelect = (index) => {
  router.push(index)
}

/**
 * 下拉菜单命令处理函数
 * @param {string} command - 命令标识（profile/logout）
 * 功能：处理用户下拉菜单的各种操作
 */
const handleCommand = async (command) => {
  // 处理退出登录命令
  if (command === 'logout') {
    try {
      // 弹出确认对话框
      await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      // 调用退出登录接口
      await logout()
      // 清除本地存储的token
      localStorage.removeItem('token')
      // 清除本地存储的用户信息
      localStorage.removeItem('userInfo')
      // 显示退出成功提示
      ElMessage.success('退出成功')
      // 跳转到登录页
      router.push('/login')
    } catch (error) {
      // 如果不是用户取消操作（即发生了错误），也清除本地存储并跳转到登录页
      if (error !== 'cancel') {
        localStorage.removeItem('token')
        localStorage.removeItem('userInfo')
        router.push('/login')
      }
    }
  }
}
</script>

<style scoped>
/* 整体布局容器样式 - 占满整个视口高度 */
.layout-container {
  height: 100vh;
}

/* 左侧侧边栏样式 - 深色背景 */
.layout-aside {
  background-color: #304156;
  overflow: hidden;
}

/* Logo区域样式 - 居中显示，白色文字 */
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  gap: 10px;
  background-color: #2b3648;
}

/* 导航菜单样式 - 去除右边框 */
.layout-menu {
  border-right: none;
}

/* 顶部头部样式 - 白色背景，底部边框，左右布局 */
.layout-header {
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

/* 页面标题样式 */
.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

/* 头部右侧区域样式 - 垂直居中对齐 */
.header-right {
  display: flex;
  align-items: center;
}

/* 用户信息样式 - 可点击，鼠标悬停显示手型 */
.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #606266;
}

/* 主内容区域样式 - 浅灰色背景，内边距 */
.layout-main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
