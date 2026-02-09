import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor - add session token
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.session?.sessionToken) {
      config.headers['X-Session-Token'] = authStore.session.sessionToken
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    if (error.response) {
      // 401 Unauthorized - session expired
      if (error.response.status === 401) {
        const authStore = useAuthStore()
        authStore.logout()
        router.push('/login')
        return Promise.reject(new Error('세션이 만료되었습니다'))
      }
      
      // Other HTTP errors
      const message = error.response.data?.message || error.response.data?.detail || '서버 오류가 발생했습니다'
      return Promise.reject(new Error(message))
    } else if (error.request) {
      // Network error - retry once
      if (!error.config._retry) {
        error.config._retry = true
        await new Promise(resolve => setTimeout(resolve, 1000))
        return api.request(error.config)
      }
      return Promise.reject(new Error('네트워크 연결을 확인해주세요'))
    } else {
      return Promise.reject(error)
    }
  }
)

export default api
