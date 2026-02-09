import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    redirect: '/menu'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/menu',
    name: 'Menu',
    component: () => import('@/views/MenuView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/cart',
    name: 'Cart',
    component: () => import('@/views/CartView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/orders',
    name: 'OrderHistory',
    component: () => import('@/views/OrderHistoryView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.session) {
    next('/login')
  } else if (to.path === '/login' && authStore.session) {
    next('/menu')
  } else {
    next()
  }
})

export default router
