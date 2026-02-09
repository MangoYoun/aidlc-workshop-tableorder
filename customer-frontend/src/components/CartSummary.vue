<template>
  <div class="card bg-gray-50">
    <div class="flex justify-between items-center">
      <span class="text-lg font-semibold">총 금액</span>
      <span class="text-2xl font-bold text-primary">{{ formatPrice(totalAmount) }}원</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  totalAmount: {
    type: Number,
    required: true
  }
})

const formatPrice = (price) => {
  return price.toLocaleString('ko-KR')
}
</script>
