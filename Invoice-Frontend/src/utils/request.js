/**
 * @description Axios HTTP 请求封装工具
 * 主要功能：
 * 1. 创建自定义配置的 Axios 实例（baseURL、超时时间等）
 * 2. 配置请求拦截器：自动在请求头中添加 Authorization token
 * 3. 配置响应拦截器：统一处理响应数据、错误提示、401 登录过期处理
 * 4. 导出封装好的请求实例，供业务代码使用
 */

// 导入 axios 库，用于发送 HTTP 请求
import axios from 'axios'
// 从 element-plus 导入消息提示组件，用于显示请求成功/失败的提示
import { ElMessage } from 'element-plus'
// 导入路由实例，用于在登录过期时跳转到登录页
import router from '@/router'

// 创建 axios 实例，配置基础参数
// 所有通过此实例发送的请求都会自动应用以下配置
const request = axios.create({
  baseURL: '/api',  // 基础请求URL，所有请求的URL都会自动加上此前缀
                    // 通常配合 Vite 的代理配置使用，解决跨域问题
  timeout: 10000    // 请求超时时间，单位为毫秒（10秒）
                    // 超过这个时间请求还未完成就会触发超时错误
})

/**
 * 请求拦截器
 * 在请求发送前执行，主要用于：
 * 1. 统一添加请求头（如 token）
 * 2. 统一处理请求参数格式
 * 3. 显示加载动画等
 */
request.interceptors.request.use(
  // 请求成功的拦截处理函数
  (config) => {
    // 从本地存储中获取 token
    const token = localStorage.getItem('token')
    // 如果 token 存在，则在请求头中添加 Authorization 字段
    // 格式为 Bearer token，这是 JWT 认证的标准格式
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    // 返回配置对象，请求继续发送
    return config
  },
  // 请求失败的拦截处理函数（一般是请求配置错误等）
  (error) => {
    // 将错误向下传递，由调用方的 catch 捕获处理
    return Promise.reject(error)
  }
)

/**
 * 响应拦截器
 * 在接收到响应后、数据返回给调用方之前执行，主要用于：
 * 1. 统一处理响应数据格式
 * 2. 统一处理业务错误（如后端返回的错误码）
 * 3. 统一处理 HTTP 错误（如 401、403、500 等）
 * 4. 统一的错误提示
 */
request.interceptors.response.use(
  // 响应成功的拦截处理函数（HTTP 状态码为 2xx 时触发）
  (response) => {
    // 获取响应数据（后端返回的实际数据）
    const res = response.data
    
    // 判断业务状态码，这里约定 code === 200 表示业务处理成功
    if (res.code === 200) {
      // 业务成功，直接返回 data 字段中的数据（剥离外层的 code 和 message）
      // 这样业务代码拿到的就是纯粹的数据，不用每次都判断 code
      return res.data
    } else {
      // 业务失败，使用 Element Plus 的消息组件显示错误提示
      ElMessage.error(res.message || '请求失败')
      // 抛出错误，由调用方的 catch 捕获处理
      return Promise.reject(new Error(res.message || '请求失败'))
    }
  },
  // 响应失败的拦截处理函数（HTTP 状态码非 2xx 时触发，如 401、404、500 等）
  (error) => {
    // 判断 HTTP 状态码是否为 401（未授权/登录过期）
    if (error.response?.status === 401) {
      // 登录过期或未授权，清除本地存储的 token 和用户信息
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      // 跳转到登录页面，让用户重新登录
      router.push('/login')
      // 显示登录过期提示
      ElMessage.error('登录已过期，请重新登录')
    } else {
      // 其他错误，显示错误提示
      // 优先显示后端返回的错误消息，其次显示 axios 自带的错误消息，最后显示默认提示
      ElMessage.error(error.response?.data?.message || error.message || '网络错误')
    }
    // 将错误向下传递，由调用方的 catch 捕获处理
    return Promise.reject(error)
  }
)

// 导出封装好的 axios 实例，供业务代码使用
// 使用方式：import request from '@/utils/request'
// 然后：request.get('/xxx') 或 request.post('/xxx', data)
export default request
