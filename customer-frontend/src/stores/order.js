import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'
import { useCartStore } from './cart'

export const useOrderStore = defineStore('order', () => {
  const orders = ref([])
  const loading = ref(false)
  const error = ref(null)

  const createOrder = async () => {
    const cartStore = useCartStore()
    
    if (cartStore.items.length === 0) {
      throw new Error('장바구니가 비어있습니다')
    }
    
    loading.value = true
    error.value = null
    
    try {
      const response = await api.post('/api/orders', {
        items: cartStore.items.map(item => ({
          menu_id: item.menuId,
          quantity: item.quantity
        })),
        total_amount: cartStore.totalAmount
      })
      
      // Clear cart on success
      cartStore.clear()
      
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const loadOrders = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.get('/api/orders')
      orders.value = response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    orders,
    loading,
    error,
    createOrder,
    loadOrders
  }
})
