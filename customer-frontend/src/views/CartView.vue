<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold mb-6">장바구니</h1>

    <div v-if="cartStore.items.length === 0" class="text-center py-12">
      <p class="text-gray-500 mb-4">장바구니가 비어있습니다</p>
      <router-link to="/menu" class="btn btn-primary">
        메뉴 보러가기
      </router-link>
    </div>

    <div v-else>
      <div class="space-y-4 mb-6">
        <CartItem
          v-for="item in cartStore.items"
          :key="item.menuId"
          :item="item"
          @update-quantity="cartStore.updateQuantity"
          @remove="cartStore.removeItem"
        />
      </div>

      <CartSummary :total-amount="cartStore.totalAmount" />

      <div class="mt-6 space-y-3">
        <button
          class="btn btn-success w-full"
          @click="showConfirmModal = true"
        >
          주문하기
        </button>
        
        <button
          class="btn btn-secondary w-full"
          @click="handleClearCart"
        >
          전체 삭제
        </button>
      </div>
    </div>

    <OrderConfirmModal
      v-if="showConfirmModal"
      :items="cartStore.items"
      :total-amount="cartStore.totalAmount"
      :loading="orderStore.loading"
      @confirm="handleCreateOrder"
      @cancel="showConfirmModal = false"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useOrderStore } from '@/stores/order'
import { useToast } from '@/composables/useToast'
import CartItem from '@/components/CartItem.vue'
import CartSummary from '@/components/CartSummary.vue'
import OrderConfirmModal from '@/components/OrderConfirmModal.vue'

const router = useRouter()
const cartStore = useCartStore()
const orderStore = useOrderStore()
const { showToast } = useToast()

const showConfirmModal = ref(false)

const handleClearCart = () => {
  if (confirm('장바구니를 비우시겠습니까?')) {
    cartStore.clear()
    showToast('장바구니가 비워졌습니다', 'info')
  }
}

const handleCreateOrder = async () => {
  try {
    const order = await orderStore.createOrder()
    showToast(`주문이 완료되었습니다 (주문번호: ${order.orderNumber})`, 'success')
    showConfirmModal.value = false
    
    setTimeout(() => {
      router.push('/menu')
    }, 2000)
  } catch (error) {
    showToast(error.message, 'error')
  }
}
</script>
