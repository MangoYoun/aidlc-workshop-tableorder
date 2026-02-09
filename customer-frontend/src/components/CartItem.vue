<template>
  <div class="card flex items-center space-x-4">
    <div class="w-20 h-20 bg-gray-200 rounded-lg overflow-hidden flex-shrink-0">
      <img
        :src="item.imageUrl || '/images/placeholder.png'"
        :alt="item.menuName"
        class="w-full h-full object-cover"
        @error="handleImageError"
      >
    </div>

    <div class="flex-1 min-w-0">
      <h3 class="font-semibold text-gray-900 truncate">{{ item.menuName }}</h3>
      <p class="text-gray-600">{{ formatPrice(item.price) }}원</p>
    </div>

    <div class="flex items-center space-x-2">
      <button
        class="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center"
        @click="$emit('update-quantity', item.menuId, item.quantity - 1)"
      >
        -
      </button>
      <span class="w-8 text-center font-semibold">{{ item.quantity }}</span>
      <button
        class="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center"
        @click="$emit('update-quantity', item.menuId, item.quantity + 1)"
      >
        +
      </button>
    </div>

    <div class="text-right">
      <p class="font-bold text-gray-900">{{ formatPrice(item.subtotal) }}원</p>
      <button
        class="text-sm text-error hover:underline"
        @click="$emit('remove', item.menuId)"
      >
        삭제
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    required: true
  }
})

defineEmits(['update-quantity', 'remove'])

const formatPrice = (price) => {
  return price.toLocaleString('ko-KR')
}

const handleImageError = (event) => {
  event.target.src = '/images/placeholder.png'
}
</script>
