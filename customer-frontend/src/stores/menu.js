import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useMenuStore = defineStore('menu', () => {
  const menus = ref([])
  const categories = ref([])
  const selectedCategoryId = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const filteredMenus = computed(() => {
    if (!selectedCategoryId.value) return menus.value
    return menus.value.filter(menu => menu.categoryId === selectedCategoryId.value)
  })

  const loadMenus = async (storeId) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/api/menus?store_id=${storeId}`)
      menus.value = response.data.menus || []
      categories.value = response.data.categories || []
      
      // Select first category by default
      if (categories.value.length > 0 && !selectedCategoryId.value) {
        selectedCategoryId.value = categories.value[0].id
      }
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const selectCategory = (categoryId) => {
    selectedCategoryId.value = categoryId
  }

  return {
    menus,
    categories,
    selectedCategoryId,
    loading,
    error,
    filteredMenus,
    loadMenus,
    selectCategory
  }
})
