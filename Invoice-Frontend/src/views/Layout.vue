<!--
  组件名称：Layout.vue
  组件用途：系统主布局组件（支持PC+移动端响应式）
  功能说明：
    - 提供系统整体布局结构（侧边栏 + 头部 + 主内容区）
    - PC端：左侧固定侧边栏 + 顶部导航 + 主内容区
    - 移动端：顶部汉堡菜单按钮 + 抽屉式侧边栏 + 主内容区
    - 左侧导航菜单，支持页面切换
    - 顶部头部显示当前页面标题和用户信息
    - 用户下拉菜单（个人信息、退出登录）
    - 主内容区通过router-view渲染子页面
-->
<template>
  <!-- 整体布局容器 - 使用Element Plus的Container布局组件 -->
  <el-container class="layout-container">
    <!-- ========== PC端左侧侧边栏（仅在PC端显示） ========== -->
    <el-aside :width="isMobile ? '0px' : '220px'" class="layout-aside" v-show="!isMobile">
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

    <!-- ========== 移动端抽屉式侧边栏 ========== -->
    <el-drawer
      v-model="drawerVisible"
      direction="ltr"
      size="260px"
      :with-header="false"
      class="mobile-drawer"
    >
      <!-- 抽屉内Logo区域 -->
      <div class="drawer-logo">
        <el-icon :size="28"><Document /></el-icon>
        <span>发票管理系统</span>
      </div>
      <!-- 抽屉内导航菜单 -->
      <el-menu
        :default-active="activeMenu"
        class="drawer-menu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        @select="handleDrawerMenuSelect"
      >
        <el-menu-item index="/dashboard">
          <el-icon><HomeFilled /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/invoice">
          <el-icon><Document /></el-icon>
          <span>发票管理</span>
        </el-menu-item>
        <el-menu-item index="/archive">
          <el-icon><Folder /></el-icon>
          <span>归档管理</span>
        </el-menu-item>
        <el-menu-item index="/user">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
      <!-- 抽屉底部用户信息 -->
      <div class="drawer-footer">
        <div class="drawer-user">
          <el-icon :size="20"><UserFilled /></el-icon>
          <span>{{ userInfo.real_name || '用户' }}</span>
        </div>
        <el-button type="danger" plain size="small" @click="handleLogout">
          退出登录
        </el-button>
      </div>
    </el-drawer>

    <!-- 右侧主容器 - 包含头部和主内容区 -->
    <el-container>
      <!-- 顶部头部栏 -->
      <el-header class="layout-header" :class="{ 'mobile-header': isMobile }">
        <!-- 头部左侧 - 汉堡菜单按钮（移动端）+ 页面标题 -->
        <div class="header-left">
          <!-- 移动端汉堡菜单按钮 -->
          <el-button
            v-if="isMobile"
            class="hamburger-btn"
            :icon="Menu"
            circle
            size="small"
            @click="drawerVisible = true"
          />
          <span class="page-title">{{ pageTitle }}</span>
        </div>
        <!-- 头部右侧 - 用户信息下拉菜单（PC端） -->
        <div class="header-right" v-if="!isMobile">
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
        <!-- 移动端头部右侧 - 简化的用户图标 -->
        <div class="header-right" v-else>
          <el-icon :size="20" class="mobile-user-icon"><UserFilled /></el-icon>
        </div>
      </el-header>
      <!-- 主内容区域 - 通过router-view渲染子页面 -->
      <el-main class="layout-main" :class="{ 'mobile-main': isMobile }">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
// 导入Vue组合式API - ref定义响应式数据，computed计算属性，onMounted生命周期钩子，onUnmounted卸载钩子，onMounted挂载钩子
import { ref, computed, onMounted, onUnmounted } from 'vue'
// 导入Vue路由 - useRoute获取当前路由信息，useRouter进行路由跳转
import { useRoute, useRouter } from 'vue-router'
// 导入Element Plus组件 - ElMessage消息提示，ElMessageBox确认对话框
import { ElMessage, ElMessageBox } from 'element-plus'
// 导入图标组件
import { Menu } from '@element-plus/icons-vue'
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

// 移动端抽屉菜单显示状态
const drawerVisible = ref(false)

// 是否为移动端（屏幕宽度小于等于768px）
const isMobile = ref(false)

// 监听窗口大小变化，判断是否为移动端
const handleResize = () => {
  isMobile.value = window.innerWidth <= 768
}

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
 * 功能：
 * 1. 从本地存储中读取用户信息并赋值
 * 2. 初始化移动端检测
 * 3. 监听窗口大小变化
 */
onMounted(() => {
  // 从localStorage获取用户信息
  const info = localStorage.getItem('userInfo')
  // 如果存在用户信息，则解析并赋值
  if (info) {
    userInfo.value = JSON.parse(info)
  }

  // 初始化移动端检测
  handleResize()
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
})

/**
 * 组件卸载生命周期钩子
 * 功能：移除窗口大小变化监听，防止内存泄漏
 */
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

/**
 * PC端菜单选择处理函数
 * @param {string} index - 菜单项的索引（路由路径）
 * 功能：点击菜单项时跳转到对应页面
 */
const handleMenuSelect = (index) => {
  router.push(index)
}

/**
 * 移动端抽屉菜单选择处理函数
 * @param {string} index - 菜单项的索引（路由路径）
 * 功能：点击菜单项时跳转到对应页面，并关闭抽屉
 */
const handleDrawerMenuSelect = (index) => {
  router.push(index)
  drawerVisible.value = false
}

/**
 * 退出登录处理函数（移动端抽屉底部按钮）
 */
const handleLogout = async () => {
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
    // 关闭抽屉
    drawerVisible.value = false
    // 显示退出成功提示
    ElMessage.success('退出成功')
    // 跳转到登录页
    router.push('/login')
  } catch (error) {
    // 如果不是用户取消操作（即发生了错误），也清除本地存储并跳转到登录页
    if (error !== 'cancel') {
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      drawerVisible.value = false
      router.push('/login')
    }
  }
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
  transition: width 0.3s ease;
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
  height: 60px;
}

/* 页面标题样式 */
.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

/* 头部左侧区域样式 - 垂直居中对齐 */
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
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
  overflow-y: auto;
}

/* ========== 移动端抽屉样式 ========== */
.mobile-drawer :deep(.el-drawer) {
  background-color: #304156;
}

.mobile-drawer :deep(.el-drawer__body) {
  padding: 0;
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* 抽屉Logo区域 */
.drawer-logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  gap: 10px;
  background-color: #2b3648;
  flex-shrink: 0;
}

/* 抽屉菜单样式 */
.drawer-menu {
  border-right: none;
  flex: 1;
  overflow-y: auto;
}

/* 抽屉底部用户信息 */
.drawer-footer {
  padding: 16px;
  border-top: 1px solid #3d4a5e;
  background-color: #2b3648;
  flex-shrink: 0;
}

.drawer-user {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #fff;
  margin-bottom: 12px;
  font-size: 14px;
}

/* ========== 移动端响应式样式 ========== */
@media screen and (max-width: 768px) {
  /* 移动端头部样式 */
  .mobile-header {
    padding: 0 12px;
    height: 56px;
  }

  /* 移动端汉堡按钮 */
  .hamburger-btn {
    background-color: #f5f7fa;
    border: none;
  }

  /* 移动端页面标题 */
  .page-title {
    font-size: 16px;
  }

  /* 移动端用户图标 */
  .mobile-user-icon {
    color: #606266;
  }

  /* 移动端主内容区 - 减少内边距 */
  .mobile-main {
    padding: 12px;
  }
}

/* 小屏幕适配 */
@media screen and (max-width: 480px) {
  .mobile-header {
    padding: 0 10px;
    height: 52px;
  }

  .page-title {
    font-size: 15px;
  }

  .mobile-main {
    padding: 10px;
  }
}
</style>
