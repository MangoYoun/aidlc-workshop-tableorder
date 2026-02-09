<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="$emit('close')">
      <div class="bg-white rounded-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex justify-between items-start mb-4">
            <h2 class="text-2xl font-bold">주문 상세</h2>
            <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="space-y-4 mb-6">
            <div>
              <p class="text-sm text-gray-600">주문번호</p>
              <p class="font-semibold">{{ order.orderNumber }}</p>
            </div>

            <div>
              <p class="text-sm text-gray-600">주문 시각</p>
              <p class="font-semibold">{{ formatDateTime(order.createdAt) }}</p>
            </div>

            <div>
              <p class="text-sm text-gray-600">주문 상태</p>
              <span
                class="inline-block px-3 py-1 rounded-full text-sm font-medium"
                :class="statusClass"
              >
                {{ order.status }}
              </span>
            </div>
          </div>

          <div class="border-t pt-4 mb-4">
            <h3 class="font-semibold mb-3">주문 내역</h3>
            <div class="space-y-2">
              <div
                v-for="item in order.items"
                :key="item.menuId"
                class="flex justify-between text-sm"
              >
                <span>{{ item.menuName }} x {{ item.quantity }}</span>
                <span class="font-semibold">{{ formatPrice(item.price * item.quantity) }}원</span>
              </div>
            </div>
          </div>

          <div class="border-t pt-4">
            <div class="flex justify-between items-center">
              <span class="text-lg font-semibold">총 금액</span>
              <span class="text-2xl font-bold text-primary">{{ formatPrice(order.totalAmount) }}원</span>
            </div>
          </div>

          <button class="btn btn-secondary w-full mt-6" @click="$emit('close')">
            닫기
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  order: {
    type: Object,
    required: true
  }
})

defineEmits(['close'])

const statusClass = computed(() => {
  const classes = {
    '대기중': 'bg-warning text-white',
    '준비중': 'bg-info text-white',
    '완료': 'bg-success text-white'
  }
  return classes[props.order.status] || 'bg-gray-500 text-white'
})

const formatPrice = (price) => {
  return price.toLocaleString('ko-KR')
}

const formatDateTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
