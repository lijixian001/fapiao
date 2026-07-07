<!--
  组件名称：Login.vue
  组件用途：企业发票管理业务系统的登录页面（支持PC+移动端响应式）
  功能说明：
    - 提供用户登录表单（用户名、密码）
    - 表单验证功能
    - 调用登录接口进行身份认证
    - 登录成功后保存token和用户信息到本地存储
    - 登录成功后跳转到系统首页
    - PC端：居中卡片，固定宽度
    - 移动端：全屏适配，卡片宽度自适应
-->
<template>
  <!-- 登录页面容器 -->
  <div class="login-container">
    <!-- 登录卡片 -->
    <el-card class="login-card">
      <!-- 登录标题区域 -->
      <div class="login-title">
        <div class="login-logo">
          <el-icon :size="40"><Document /></el-icon>
        </div>
        <h2>企业发票管理业务系统</h2>
        <p>Enterprise Invoice Management System</p>
      </div>
      <!-- 登录表单 -->
      <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" label-width="0" class="login-form">
        <!-- 用户名输入框 -->
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            size="large"
            prefix-icon="User"
          />
        </el-form-item>
        <!-- 密码输入框 -->
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
        <!-- 登录按钮 -->
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-btn"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      <!-- 登录提示信息 -->
      <div class="login-tip">
        <span>默认账号: 123 / 123</span>
      </div>
    </el-card>
  </div>
</template>

<script setup>
// 导入Vue响应式API
import { ref, reactive } from 'vue'
// 导入Vue路由
import { useRouter } from 'vue-router'
// 导入Element Plus消息提示组件
import { ElMessage } from 'element-plus'
// 导入登录API接口
import { login } from '@/api/auth'

// 获取路由实例
const router = useRouter()
// 登录表单引用
const loginFormRef = ref(null)
// 登录按钮加载状态
const loading = ref(false)

// 登录表单数据
const loginForm = reactive({
  username: '123',
  password: '123'
})

// 登录表单验证规则
const loginRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

/**
 * 登录处理函数
 */
const handleLogin = async () => {
  try {
    await loginFormRef.value.validate()
    loading.value = true
    const res = await login(loginForm)
    localStorage.setItem('token', res.token)
    localStorage.setItem('userInfo', JSON.stringify(res.user_info))
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error) {
    console.error('登录失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* 登录页面容器样式 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  height: 100%;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-sizing: border-box;
}

/* 登录卡片样式 */
.login-card {
  width: 400px;
  max-width: 100%;
  padding: 30px 25px;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  box-sizing: border-box;
}

/* 登录标题区域样式 */
.login-title {
  text-align: center;
  margin-bottom: 30px;
}

/* 登录Logo图标 */
.login-logo {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

/* 主标题样式 */
.login-title h2 {
  color: #303133;
  font-size: 22px;
  margin-bottom: 6px;
  font-weight: 600;
}

/* 副标题样式 */
.login-title p {
  color: #909399;
  font-size: 13px;
}

/* 登录表单 */
.login-form {
  width: 100%;
}

/* 登录按钮 */
.login-btn {
  width: 100%;
  min-height: 48px;
  font-size: 16px;
}

/* 登录提示文字样式 */
.login-tip {
  text-align: center;
  color: #909399;
  font-size: 12px;
  margin-top: 16px;
}

/* ========== 移动端响应式样式（<=768px） ========== */
@media screen and (max-width: 768px) {
  .login-container {
    padding: 16px;
    align-items: flex-start;
    padding-top: 15vh;
  }

  .login-card {
    width: 100%;
    max-width: 400px;
    padding: 24px 20px;
  }

  .login-title {
    margin-bottom: 24px;
  }

  .login-logo {
    width: 56px;
    height: 56px;
    margin-bottom: 12px;
  }

  .login-title h2 {
    font-size: 20px;
  }

  .login-btn {
    min-height: 48px;
  }
}

/* ========== 小屏幕适配（<=480px） ========== */
@media screen and (max-width: 480px) {
  .login-container {
    padding: 12px;
    padding-top: 12vh;
  }

  .login-card {
    padding: 20px 16px;
    border-radius: 10px;
  }

  .login-title {
    margin-bottom: 20px;
  }

  .login-logo {
    width: 52px;
    height: 52px;
    margin-bottom: 10px;
  }

  .login-title h2 {
    font-size: 18px;
  }

  .login-title p {
    font-size: 12px;
  }
}

/* ========== 横屏适配（移动端横屏） ========== */
@media screen and (max-height: 500px) and (orientation: landscape) {
  .login-container {
    padding-top: 20px;
    align-items: flex-start;
  }

  .login-card {
    padding: 16px 20px;
  }

  .login-title {
    margin-bottom: 16px;
  }

  .login-logo {
    width: 44px;
    height: 44px;
    margin-bottom: 8px;
  }

  .login-title h2 {
    font-size: 18px;
    margin-bottom: 4px;
  }
}
</style>
