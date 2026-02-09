<template>
  <div class="text-center py-12">
    <p class="text-error mb-4">{{ message }}</p>
    <button v-if="showRetry" class="btn btn-primary" @click="$emit('retry')">
      다시 시도
    </button>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    required: true
  },
  showRetry: {
    type: Boolean,
    default: true
  }
})

defineEmits(['retry'])
</script>
