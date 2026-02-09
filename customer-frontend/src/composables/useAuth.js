import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

export const useAuth = () => {
  const authStore = useAuthStore()

  const isLoggedIn = computed(() => !!authStore.session)
  const session = computed(() => authStore.session)

  return {
    isLoggedIn,
    session
  }
}
