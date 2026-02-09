<template>
  <div
    class="card cursor-pointer hover:shadow-lg transition-shadow"
    :class="{ 'opacity-50': !menu.isAvailable }"
    @click="$emit('click')"
  >
    <div class="aspect-square bg-gray-200 rounded-lg mb-3 overflow-hidden">
      <img
        :src="menu.imageUrl || '/images/placeholder.png'"
        :alt="menu.name"
        class="w-full h-full object-cover"
        @error="handleImageError"
      >
    </div>
    
    <h3 class="font-semibold text-gray-900 mb-1">{{ menu.name }}</h3>
    <p class="text-primary font-bold">{{ formatPrice(menu.price) }}원</p>
    
    <div v-if="!menu.isAvailable" class="mt-2">
      <span class="text-xs bg-gray-500 text-white px-2 py-1 rounded">품절</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  menu: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])

const formatPrice = (price) => {
  return price.toLocaleString('ko-KR')
}

const handleImageError = (event) => {
  event.target.src = '/images/placeholder.png'
}
</script>
