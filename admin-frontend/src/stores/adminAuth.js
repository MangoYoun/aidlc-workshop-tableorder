import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

export const useAdminAuthStore = defineStore('adminAuth', () => {
  const token = ref(null)
  const user = ref(null)

  const loadAuth = () => {
    const data = localStorage.getItem('admin_token')
    if (data) {
      try {
        const parsed = JSON.parse(data)
        if (new Date(parsed.expiresAt) > new Date()) {
          token.value = parsed.token
          user.value = parsed.user
        } else {
          localStorage.removeItem('admin_token')
        }
      } catch (error) {
        console.error('Failed to parse admin token:', error)
        localStorage.removeItem('admin_token')
      }
    }
  }

  const login = async (storeId, username, password) => {
    try {
      const response = await api.post('/api/auth/admin-login', {
        store_id: storeId,
        username,
        password
      })
      
      token.value = response.data.token
      user.value = response.data.user
      
      localStorage.setItem('admin_token', JSON.stringify({
        token: response.data.token,
        user: response.data.user,
        expiresAt: response.data.expiresAt
      }))
      
      return response.data
    } catch (error) {
      throw error
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('admin_token')
  }

  return {
    token,
    user,
    loadAuth,
    login,
    logout
  }
})
