<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold mb-6">주문 내역</h1>

    <LoadingSpinner v-if="orderStore.loading" />
    
    <ErrorMessage
      v-else-if="orderStore.error"
      :message="orderStore.error"
      @retry="loadOrders"
    />

    <div v-else-if="orderStore.orders.length === 0" class="text-center py-12">
      <p class="text-gray-500 mb-4">주문 내역이 없습니다</p>
      <router-link to="/menu" class="btn btn-primary">
        메뉴 보러가기
      </router-link>
    </div>

    <div v-else class="space-y-4">
      <OrderCard
        v-for="order in orderStore.orders"
        :key="order.id"
        :order="order"
        @click="openOrderDetail(order)"
      />
    </div>

    <OrderDetailModal
      v-if="selectedOrder"
      :order="selectedOrder"
      @close="selectedOrder = null"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useOrderStore } from '@/stores/order'
import OrderCard from '@/components/OrderCard.vue'
import OrderDetailModal from '@/components/OrderDetailModal.vue'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'
import ErrorMessage from '@/components/shared/ErrorMessage.vue'

const orderStore = useOrderStore()
const selectedOrder = ref(null)

const loadOrders = async () => {
  try {
    await orderStore.loadOrders()
  } catch (error) {
    console.error('Failed to load orders:', error)
  }
}

const openOrderDetail = (order) => {
  selectedOrder.value = order
}

onMounted(() => {
  loadOrders()
})
</script>
