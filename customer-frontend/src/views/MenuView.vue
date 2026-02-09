<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold mb-6">메뉴</h1>

    <LoadingSpinner v-if="menuStore.loading" />
    
    <ErrorMessage
      v-else-if="menuStore.error"
      :message="menuStore.error"
      @retry="loadMenus"
    />

    <div v-else>
      <CategoryTabs
        :categories="menuStore.categories"
        :selected-id="menuStore.selectedCategoryId"
        @select="menuStore.selectCategory"
      />

      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mt-6">
        <MenuCard
          v-for="menu in menuStore.filteredMenus"
          :key="menu.id"
          :menu="menu"
          @click="openMenuDetail(menu)"
        />
      </div>

      <div v-if="menuStore.filteredMenus.length === 0" class="text-center py-12 text-gray-500">
        이 카테고리에 메뉴가 없습니다
      </div>
    </div>

    <MenuDetailModal
      v-if="selectedMenu"
      :menu="selectedMenu"
      @close="selectedMenu = null"
      @add-to-cart="handleAddToCart"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMenuStore } from '@/stores/menu'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import CategoryTabs from '@/components/CategoryTabs.vue'
import MenuCard from '@/components/MenuCard.vue'
import MenuDetailModal from '@/components/MenuDetailModal.vue'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'
import ErrorMessage from '@/components/shared/ErrorMessage.vue'

const menuStore = useMenuStore()
const cartStore = useCartStore()
const authStore = useAuthStore()
const { showToast } = useToast()

const selectedMenu = ref(null)

const loadMenus = async () => {
  try {
    await menuStore.loadMenus(authStore.session.storeId)
  } catch (error) {
    console.error('Failed to load menus:', error)
  }
}

const openMenuDetail = (menu) => {
  if (menu.isAvailable) {
    selectedMenu.value = menu
  }
}

const handleAddToCart = (menu, quantity) => {
  cartStore.addItem(menu, quantity)
  showToast('장바구니에 추가되었습니다', 'success')
  selectedMenu.value = null
}

onMounted(() => {
  cartStore.loadCart()
  loadMenus()
})
</script>
