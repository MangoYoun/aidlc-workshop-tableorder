import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const session = ref(null)

  const loadSession = () => {
    const data = localStorage.getItem('table_session')
    if (data) {
      try {
        const parsed = JSON.parse(data)
        // Check if session is expired
        if (new Date(parsed.expiresAt) > new Date()) {
          session.value = parsed
        } else {
          // Session expired
          localStorage.removeItem('table_session')
          session.value = null
        }
      } catch (error) {
        console.error('Failed to parse session:', error)
        localStorage.removeItem('table_session')
      }
    }
  }

  const login = async (storeId, tableNumber, password) => {
    try {
      const response = await api.post('/api/auth/table-login', {
        store_id: storeId,
        table_number: tableNumber,
        password
      })
      
      session.value = response.data
      localStorage.setItem('table_session', JSON.stringify(response.data))
      return response.data
    } catch (error) {
      throw error
    }
  }

  const logout = () => {
    session.value = null
    localStorage.removeItem('table_session')
    localStorage.removeItem('cart_items')
  }

  const checkSession = () => {
    if (session.value) {
      const expiresAt = new Date(session.value.expiresAt)
      if (expiresAt <= new Date()) {
        logout()
        return false
      }
      return true
    }
    return false
  }

  return {
    session,
    loadSession,
    login,
    logout,
    checkSession
  }
})
