<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="$emit('cancel')">
      <div class="bg-white rounded-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <h2 class="text-2xl font-bold mb-4">주문 확인</h2>

          <div class="space-y-3 mb-6">
            <div
              v-for="item in items"
              :key="item.menuId"
              class="flex justify-between text-sm"
            >
              <span>{{ item.menuName }} x {{ item.quantity }}</span>
              <span class="font-semibold">{{ formatPrice(item.subtotal) }}원</span>
            </div>
          </div>

          <div class="border-t pt-4 mb-6">
            <div class="flex justify-between items-center">
              <span class="text-lg font-semibold">총 금액</span>
              <span class="text-2xl font-bold text-primary">{{ formatPrice(totalAmount) }}원</span>
            </div>
          </div>

          <div class="space-y-3">
            <button
              class="btn btn-success w-full"
              :disabled="loading"
              @click="$emit('confirm')"
            >
              {{ loading ? '주문 중...' : '주문 확정' }}
            </button>
            
            <button
              class="btn btn-secondary w-full"
              :disabled="loading"
              @click="$emit('cancel')"
            >
              취소
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    required: true
  },
  totalAmount: {
    type: Number,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['confirm', 'cancel'])

const formatPrice = (price) => {
  return price.toLocaleString('ko-KR')
}
</script>
