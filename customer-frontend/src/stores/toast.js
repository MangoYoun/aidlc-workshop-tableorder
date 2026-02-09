import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useToastStore = defineStore('toast', () => {
  const toast = ref(null)

  const show = (message, type = 'info') => {
    toast.value = { message, type }
  }

  return {
    toast,
    show
  }
})
