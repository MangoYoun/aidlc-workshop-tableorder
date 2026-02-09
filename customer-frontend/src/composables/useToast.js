import { useToastStore } from '@/stores/toast'

export const useToast = () => {
  const toastStore = useToastStore()

  const showToast = (message, type = 'info') => {
    toastStore.show(message, type)
  }

  return {
    showToast
  }
}
