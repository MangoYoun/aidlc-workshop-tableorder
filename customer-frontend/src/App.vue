<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <AppHeader v-if="isLoggedIn" />
    <main class="main-content">
      <RouterView />
    </main>
    <Toast />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/shared/AppHeader.vue'
import Toast from '@/components/shared/Toast.vue'

const authStore = useAuthStore()
const isLoggedIn = computed(() => !!authStore.session)

onMounted(() => {
  authStore.loadSession()
})
</script>

<style>
.main-content {
  padding-bottom: 1rem;
}
</style>
