/**
 * @description Vue Router 路由配置文件
 * 主要功能：
 * 1. 定义应用的路由表，配置各个页面对应的路径和组件
 * 2. 创建路由实例，使用 HTML5 History 模式
 * 3. 配置全局前置守卫，实现登录权限验证
 * 4. 导出路由实例供应用使用
 */

// 从 vue-router 库中导入创建路由实例和历史模式的函数
// createRouter: 用于创建路由实例
// createWebHistory: 用于创建 HTML5 History 模式的历史记录（URL更美观，无#号）
import { createRouter, createWebHistory } from 'vue-router'

// 路由配置数组，定义应用中所有的路由规则
// 每个路由对象包含：path(路径)、name(路由名称)、component(组件)、children(子路由)等属性
const routes = [
  // 登录页面路由
  {
    path: '/login',           // 路由路径
    name: 'Login',            // 路由名称，用于编程式导航
    component: () => import('@/views/Login.vue')  // 路由组件，使用懒加载方式导入
  },
  // 根路径重定向，访问根路径时自动跳转到仪表盘
  {
    path: '/',                // 根路径
    redirect: '/dashboard'    // 重定向目标路径
  },
  // 仪表盘主布局路由，包含侧边栏和顶部导航等布局结构
  // 所有需要登录后访问的页面都作为此路由的子路由
  {
    path: '/dashboard',       // 仪表盘路径
    name: 'Dashboard',        // 路由名称
    component: () => import('@/views/Layout.vue'),  // 布局组件，包含整体页面框架
    children: [               // 子路由配置，这些页面会在布局组件的内部渲染
      // 仪表盘首页（默认子路由，path为空表示访问/dashboard时直接渲染此组件）
      {
        path: '',
        name: 'DashboardHome',
        component: () => import('@/views/Dashboard.vue')
      },
      // 发票管理页面
      {
        path: '/invoice',
        name: 'Invoice',
        component: () => import('@/views/Invoice.vue')
      },
      // 归档管理页面
      {
        path: '/archive',
        name: 'Archive',
        component: () => import('@/views/Archive.vue')
      },
      // 用户管理页面
      {
        path: '/user',
        name: 'User',
        component: () => import('@/views/User.vue')
      }
    ]
  }
]

// 创建路由实例
const router = createRouter({
  // 使用 HTML5 History 模式，URL 更加美观（没有 # 号）
  // 需要后端配合配置，否则刷新页面会出现 404
  history: createWebHistory(),
  // 传入路由配置数组
  routes
})

/**
 * 全局前置守卫
 * 在每次路由跳转前执行，用于进行登录权限验证
 * @param {Object} to - 即将要进入的目标路由对象
 * @param {Object} from - 当前导航正要离开的路由对象
 * @param {Function} next - 回调函数，用于控制导航行为
 *   - next()：放行，进入目标路由
 *   - next('/login')：跳转到指定路径
 *   - next(false)：中断当前导航
 */
router.beforeEach((to, from, next) => {
  // 从本地存储中获取 token，用于判断用户是否已登录
  const token = localStorage.getItem('token')
  
  // 如果要访问的是登录页面，直接放行（无论是否登录都可以访问登录页）
  if (to.path === '/login') {
    next()
  } else {
    // 如果要访问其他页面，检查是否有 token
    if (!token) {
      // 没有 token，说明未登录，强制跳转到登录页面
      next('/login')
    } else {
      // 有 token，说明已登录，放行访问目标页面
      next()
    }
  }
})

// 导出路由实例，供 main.js 中使用
export default router
