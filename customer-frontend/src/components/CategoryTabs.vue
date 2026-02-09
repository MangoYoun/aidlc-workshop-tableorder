<template>
  <div class="flex overflow-x-auto space-x-2 pb-2">
    <button
      v-for="category in categories"
      :key="category.id"
      class="px-4 py-2 rounded-lg whitespace-nowrap transition-colors"
      :class="category.id === selectedId ? 'bg-primary text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
      @click="$emit('select', category.id)"
    >
      {{ category.name }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  categories: {
    type: Array,
    required: true
  },
  selectedId: {
    type: Number,
    default: null
  }
})

defineEmits(['select'])
</script>
