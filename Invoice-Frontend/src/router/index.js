import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Layout.vue'),
    children: [
      {
        path: '',
        name: 'DashboardHome',
        component: () => import('@/views/Dashboard.vue')
      },
      {
        path: '/invoice',
        name: 'Invoice',
        component: () => import('@/views/Invoice.vue')
      },
      {
        path: '/archive',
        name: 'Archive',
        component: () => import('@/views/Archive.vue')
      },
      {
        path: '/user',
        name: 'User',
        component: () => import('@/views/User.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path === '/login') {
    next()
  } else {
    if (!token) {
      next('/login')
    } else {
      next()
    }
  }
})

export default router
