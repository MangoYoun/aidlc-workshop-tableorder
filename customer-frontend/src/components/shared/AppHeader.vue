<template>
  <header class="bg-white shadow-sm sticky top-0 z-10">
    <div class="container mx-auto px-4 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-lg font-bold">{{ authStore.session?.storeName }}</h1>
          <p class="text-sm text-gray-600">{{ authStore.session?.tableName }}</p>
        </div>

        <nav class="flex items-center space-x-4">
          <router-link
            to="/menu"
            class="text-gray-700 hover:text-primary"
            active-class="text-primary font-semibold"
          >
            메뉴
          </router-link>
          
          <router-link
            to="/cart"
            class="relative text-gray-700 hover:text-primary"
            active-class="text-primary font-semibold"
          >
            장바구니
            <span
              v-if="cartStore.itemCount > 0"
              class="absolute -top-2 -right-2 bg-error text-white text-xs rounded-full w-5 h-5 flex items-center justify-center"
            >
              {{ cartStore.itemCount }}
            </span>
          </router-link>
          
          <router-link
            to="/orders"
            class="text-gray-700 hover:text-primary"
            active-class="text-primary font-semibold"
          >
            주문내역
          </router-link>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'

const authStore = useAuthStore()
const cartStore = useCartStore()
</script>
