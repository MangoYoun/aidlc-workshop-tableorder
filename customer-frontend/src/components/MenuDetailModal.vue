<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="$emit('close')">
      <div class="bg-white rounded-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex justify-between items-start mb-4">
            <h2 class="text-2xl font-bold">{{ menu.name }}</h2>
            <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="aspect-video bg-gray-200 rounded-lg mb-4 overflow-hidden">
            <img
              :src="menu.imageUrl || '/images/placeholder.png'"
              :alt="menu.name"
              class="w-full h-full object-cover"
              @error="handleImageError"
            >
          </div>

          <p v-if="menu.description" class="text-gray-600 mb-4">
            {{ menu.description }}
          </p>

          <p class="text-2xl font-bold text-primary mb-6">
            {{ formatPrice(menu.price) }}원
          </p>

          <div class="flex items-center justify-between mb-6">
            <span class="font-medium">수량</span>
            <div class="flex items-center space-x-4">
              <button
                class="w-10 h-10 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center"
                :disabled="quantity <= 1"
                @click="quantity--"
              >
                -
              </button>
              <span class="text-xl font-semibold w-8 text-center">{{ quantity }}</span>
              <button
                class="w-10 h-10 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center"
                @click="quantity++"
              >
                +
              </button>
            </div>
          </div>

          <button
            class="btn btn-primary w-full"
            :disabled="!menu.isAvailable"
            @click="handleAddToCart"
          >
            {{ menu.isAvailable ? '장바구니 담기' : '품절' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  menu: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'add-to-cart'])

const quantity = ref(1)

const formatPrice = (price) => {
  return price.toLocaleString('ko-KR')
}

const handleImageError = (event) => {
  event.target.src = '/images/placeholder.png'
}

const handleAddToCart = () => {
  emit('add-to-cart', props.menu, quantity.value)
}
</script>
