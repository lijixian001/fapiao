<!--
  组件名称：Login.vue
  组件用途：企业发票管理业务系统的登录页面
  功能说明：
    - 提供用户登录表单（用户名、密码）
    - 表单验证功能
    - 调用登录接口进行身份认证
    - 登录成功后保存token和用户信息到本地存储
    - 登录成功后跳转到系统首页
-->
<template>
  <!-- 登录页面容器 - 居中显示登录卡片 -->
  <div class="login-container">
    <!-- 登录卡片 - 使用Element Plus卡片组件 -->
    <el-card class="login-card">
      <!-- 登录标题区域 -->
      <div class="login-title">
        <h2>企业发票管理业务系统</h2>
        <p>Enterprise Invoice Management System</p>
      </div>
      <!-- 登录表单 - 绑定表单数据和验证规则 -->
      <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" label-width="0">
        <!-- 用户名输入框 -->
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            size="large"
            prefix-icon="User"
          />
        </el-form-item>
        <!-- 密码输入框 - 支持回车登录 -->
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            prefix-icon="Lock"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <!-- 登录按钮 - 点击触发登录操作 -->
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            style="width: 100%"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      <!-- 登录提示信息 - 显示默认账号 -->
      <div class="login-tip">
        <span>默认账号: 123 / 123</span>
      </div>
    </el-card>
  </div>
</template>

<script setup>
// 导入Vue响应式API - ref用于定义基本类型响应式数据，reactive用于定义对象类型响应式数据
import { ref, reactive } from 'vue'
// 导入Vue路由 - 用于页面跳转
import { useRouter } from 'vue-router'
// 导入Element Plus消息提示组件
import { ElMessage } from 'element-plus'
// 导入登录API接口
import { login } from '@/api/auth'

// 获取路由实例
const router = useRouter()
// 登录表单引用 - 用于表单验证
const loginFormRef = ref(null)
// 登录按钮加载状态 - 控制登录按钮的loading效果
const loading = ref(false)

// 登录表单数据 - 使用reactive定义响应式对象，包含用户名和密码
const loginForm = reactive({
  username: '123',
  password: '123'
})

// 登录表单验证规则 - 配置用户名和密码的必填验证
const loginRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

/**
 * 登录处理函数
 * 功能：
 *   1. 验证表单数据
 *   2. 调用登录接口
 *   3. 保存token和用户信息到本地存储
 *   4. 登录成功跳转到首页
 *   5. 处理异常情况
 */
const handleLogin = async () => {
  try {
    // 执行表单验证
    await loginFormRef.value.validate()
    // 设置加载状态为true，防止重复提交
    loading.value = true
    // 调用登录接口
    const res = await login(loginForm)
    // 保存token到本地存储
    localStorage.setItem('token', res.token)
    // 保存用户信息到本地存储
    localStorage.setItem('userInfo', JSON.stringify(res.user_info))
    // 显示登录成功提示
    ElMessage.success('登录成功')
    // 跳转到系统首页
    router.push('/')
  } catch (error) {
    // 打印登录失败错误信息
    console.error('登录失败:', error)
  } finally {
    // 无论成功失败，都重置加载状态
    loading.value = false
  }
}
</script>

<style scoped>
/* 登录页面容器样式 - 全屏居中显示，渐变背景 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 登录卡片样式 - 固定宽度，圆角，阴影效果 */
.login-card {
  width: 400px;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

/* 登录标题区域样式 - 居中对齐，底部间距 */
.login-title {
  text-align: center;
  margin-bottom: 30px;
}

/* 主标题样式 */
.login-title h2 {
  color: #303133;
  font-size: 24px;
  margin-bottom: 8px;
}

/* 副标题样式 */
.login-title p {
  color: #909399;
  font-size: 14px;
}

/* 登录提示文字样式 - 底部提示信息 */
.login-tip {
  text-align: center;
  color: #909399;
  font-size: 12px;
  margin-top: 10px;
}
</style>
