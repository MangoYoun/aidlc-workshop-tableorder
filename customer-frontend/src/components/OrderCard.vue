<template>
  <div class="card cursor-pointer hover:shadow-lg transition-shadow" @click="$emit('click')">
    <div class="flex justify-between items-start mb-3">
      <div>
        <h3 class="font-semibold text-gray-900">주문번호: {{ order.orderNumber }}</h3>
        <p class="text-sm text-gray-600">{{ formatDateTime(order.createdAt) }}</p>
      </div>
      <span
        class="px-3 py-1 rounded-full text-sm font-medium"
        :class="statusClass"
      >
        {{ order.status }}
      </span>
    </div>

    <div class="space-y-1 mb-3">
      <p
        v-for="item in order.items.slice(0, 2)"
        :key="item.menuId"
        class="text-sm text-gray-700"
      >
        {{ item.menuName }} x {{ item.quantity }}
      </p>
      <p v-if="order.items.length > 2" class="text-sm text-gray-500">
        외 {{ order.items.length - 2 }}개
      </p>
    </div>

    <p class="text-lg font-bold text-primary">
      {{ formatPrice(order.totalAmount) }}원
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  order: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])

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
