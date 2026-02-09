import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])

  const totalAmount = computed(() => {
    return items.value.reduce((sum, item) => sum + item.subtotal, 0)
  })

  const itemCount = computed(() => {
    return items.value.reduce((sum, item) => sum + item.quantity, 0)
  })

  const loadCart = () => {
    const data = localStorage.getItem('cart_items')
    if (data) {
      try {
        items.value = JSON.parse(data)
      } catch (error) {
        console.error('Failed to parse cart:', error)
        localStorage.removeItem('cart_items')
      }
    }
  }

  const saveCart = () => {
    localStorage.setItem('cart_items', JSON.stringify(items.value))
  }

  const addItem = (menu, quantity = 1) => {
    const existingItem = items.value.find(item => item.menuId === menu.id)
    
    if (existingItem) {
      existingItem.quantity += quantity
      existingItem.subtotal = existingItem.price * existingItem.quantity
    } else {
      items.value.push({
        menuId: menu.id,
        menuName: menu.name,
        price: menu.price,
        quantity,
        subtotal: menu.price * quantity,
        imageUrl: menu.imageUrl
      })
    }
    
    saveCart()
  }

  const updateQuantity = (menuId, quantity) => {
    const item = items.value.find(item => item.menuId === menuId)
    
    if (item) {
      if (quantity < 1) {
        removeItem(menuId)
      } else {
        item.quantity = quantity
        item.subtotal = item.price * quantity
        saveCart()
      }
    }
  }

  const removeItem = (menuId) => {
    items.value = items.value.filter(item => item.menuId !== menuId)
    saveCart()
  }

  const clear = () => {
    items.value = []
    localStorage.removeItem('cart_items')
  }

  return {
    items,
    totalAmount,
    itemCount,
    loadCart,
    addItem,
    updateQuantity,
    removeItem,
    clear
  }
})
