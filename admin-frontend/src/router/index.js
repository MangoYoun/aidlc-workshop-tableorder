import { createRouter, createWebHistory } from 'vue-router'
import { useAdminAuthStore } from '@/stores/adminAuth'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'AdminLogin',
    component: () => import('@/views/AdminLoginView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/OrderDashboardView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/tables',
    name: 'Tables',
    component: () => import('@/views/TableManagementView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/menus',
    name: 'Menus',
    component: () => import('@/views/MenuManagementView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAdminAuthStore()
  
  if (to.meta.requiresAuth && !authStore.token) {
    next('/login')
  } else if (to.path === '/login' && authStore.token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
