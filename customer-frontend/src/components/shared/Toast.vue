<template>
  <Teleport to="body">
    <Transition name="toast">
      <div
        v-if="visible"
        class="fixed top-4 right-4 z-50 max-w-sm"
      >
        <div
          class="rounded-lg shadow-lg p-4 text-white"
          :class="toastClass"
        >
          {{ message }}
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useToastStore } from '@/stores/toast'

const toastStore = useToastStore()

const visible = ref(false)
const message = ref('')
const type = ref('info')

const toastClass = computed(() => {
  const classes = {
    success: 'bg-success',
    error: 'bg-error',
    warning: 'bg-warning',
    info: 'bg-info'
  }
  return classes[type.value] || classes.info
})

watch(() => toastStore.toast, (newToast) => {
  if (newToast) {
    message.value = newToast.message
    type.value = newToast.type
    visible.value = true
    
    setTimeout(() => {
      visible.value = false
    }, 2000)
  }
})
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
