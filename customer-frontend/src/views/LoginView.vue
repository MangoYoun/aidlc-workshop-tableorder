<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900">테이블오더</h1>
        <p class="mt-2 text-gray-600">테이블 로그인</p>
      </div>

      <div class="card">
        <form @submit.prevent="handleLogin">
          <div class="space-y-4">
            <div>
              <label for="tableNumber" class="block text-sm font-medium text-gray-700 mb-1">
                테이블 번호
              </label>
              <input
                id="tableNumber"
                v-model="form.tableNumber"
                type="text"
                required
                class="input"
                placeholder="예: 1"
              >
            </div>

            <div>
              <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
                비밀번호
              </label>
              <input
                id="password"
                v-model="form.password"
                type="password"
                required
                minlength="4"
                class="input"
                placeholder="비밀번호를 입력하세요"
              >
            </div>

            <div v-if="errorMessage" class="text-error text-sm">
              {{ errorMessage }}
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="btn btn-primary w-full"
            >
              {{ loading ? '로그인 중...' : '로그인' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const authStore = useAuthStore()
const { showToast } = useToast()

const form = ref({
  tableNumber: '',
  password: ''
})

const loading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    await authStore.login(
      null, // store_id는 null로 전달 (Backend에서 자동 설정)
      form.value.tableNumber,
      form.value.password
    )
    
    showToast('로그인 성공', 'success')
    router.push('/menu')
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || error.message || '로그인 실패'
  } finally {
    loading.value = false
  }
}
</script>
