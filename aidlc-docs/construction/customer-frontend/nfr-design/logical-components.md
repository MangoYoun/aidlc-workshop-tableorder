# Logical Components - Customer Frontend

## Overview

Customer Frontend의 논리적 컴포넌트 구조를 정의합니다. Frontend 애플리케이션의 주요 구성 요소와 그 역할을 명시합니다.

---

## 1. Application Core (애플리케이션 코어)

### Component 1.1: Vue Application Instance
**역할**: Vue.js 애플리케이션의 진입점

**구현**:
```javascript
// main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './assets/main.css'

const app = createApp(App)

// Global Error Handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Vue Error:', err, info)
}

app.use(createPinia())
app.use(router)
app.mount('#app')
```

**책임**:
- 앱 초기화
- 플러그인 등록 (Pinia, Router)
- 전역 에러 핸들러 설정

---

### Component 1.2: Root Component (App.vue)
**역할**: 최상위 컴포넌트, 레이아웃 관리

**구현**:
```vue
<template>
  <div id="app">
    <AppHeader v-if="isLoggedIn" />
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/shared/AppHeader.vue'

const authStore = useAuthStore()
const isLoggedIn = computed(() => !!authStore.session)
</script>
```

**책임**:
- 전역 레이아웃
- 헤더 표시 여부 제어
- 라우터 뷰 렌더링

---

## 2. Routing Layer (라우팅 계층)

### Component 2.1: Vue Router
**역할**: 클라이언트 측 라우팅 관리

**구현**:
```javascript
// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    redirect: '/menu'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/menu',
    name: 'Menu',
    component: () => import('@/views/MenuView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/cart',
    name: 'Cart',
    component: () => import('@/views/CartView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/orders',
    name: 'OrderHistory',
    component: () => import('@/views/OrderHistoryView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.session) {
    next('/login')
  } else if (to.path === '/login' && authStore.session) {
    next('/menu')
  } else {
    next()
  }
})

export default router
```

**책임**:
- 라우트 정의
- 네비게이션 가드 (인증 체크)
- 페이지 전환 관리

---

## 3. State Management Layer (상태 관리 계층)

### Component 3.1: Auth Store
**역할**: 인증 및 세션 관리

**구현**:
```javascript
// stores/auth.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const session = ref(null)

  const loadSession = () => {
    const data = localStorage.getItem('table_session')
    if (data) {
      session.value = JSON.parse(data)
    }
  }

  const login = async (storeId, tableNumber, password) => {
    const response = await api.post('/api/auth/table-login', {
      store_id: storeId,
      table_number: tableNumber,
      password
    })
    session.value = response.data
    localStorage.setItem('table_session', JSON.stringify(response.data))
  }

  const logout = () => {
    session.value = null
    localStorage.removeItem('table_session')
    localStorage.removeItem('cart_items')
  }

  return { session, loadSession, login, logout }
})
```

**책임**:
- 세션 정보 관리
- 로그인/로그아웃
- LocalStorage 동기화

---

### Component 3.2: Menu Store
**역할**: 메뉴 및 카테고리 관리

**구현**:
```javascript
// stores/menu.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

export const useMenuStore = defineStore('menu', () => {
  const menus = ref([])
  const categories = ref([])
  const selectedCategoryId = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const loadMenus = async (storeId) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/api/menus?store_id=${storeId}`)
      menus.value = response.data.menus
      categories.value = response.data.categories
      if (categories.value.length > 0) {
        selectedCategoryId.value = categories.value[0].id
      }
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const selectCategory = (categoryId) => {
    selectedCategoryId.value = categoryId
  }

  return { menus, categories, selectedCategoryId, loading, error, loadMenus, selectCategory }
})
```

**책임**:
- 메뉴 데이터 관리
- 카테고리 선택 상태
- API 호출 및 에러 처리

---

### Component 3.3: Cart Store
**역할**: 장바구니 관리

**구현**:
```javascript
// stores/cart.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])

  const totalAmount = computed(() => {
    return items.value.reduce((sum, item) => sum + item.subtotal, 0)
  })

  const itemCount = computed(() => {
    return items.value.reduce((sum, item) => sum + item.quantity, 0)
  })

  const loadCart = () => {
    const data = localStorage.getItem('cart_items')
    if (data) {
      items.value = JSON.parse(data)
    }
  }

  const saveCart = () => {
    localStorage.setItem('cart_items', JSON.stringify(items.value))
  }

  const addItem = (menu, quantity = 1) => {
    const existingItem = items.value.find(item => item.menuId === menu.id)
    if (existingItem) {
      existingItem.quantity += quantity
      existingItem.subtotal = existingItem.price * existingItem.quantity
    } else {
      items.value.push({
        menuId: menu.id,
        menuName: menu.name,
        price: menu.price,
        quantity,
        subtotal: menu.price * quantity,
        imageUrl: menu.imageUrl
      })
    }
    saveCart()
  }

  const updateQuantity = (menuId, quantity) => {
    const item = items.value.find(item => item.menuId === menuId)
    if (item) {
      if (quantity < 1) {
        removeItem(menuId)
      } else {
        item.quantity = quantity
        item.subtotal = item.price * quantity
        saveCart()
      }
    }
  }

  const removeItem = (menuId) => {
    items.value = items.value.filter(item => item.menuId !== menuId)
    saveCart()
  }

  const clear = () => {
    items.value = []
    localStorage.removeItem('cart_items')
  }

  return { items, totalAmount, itemCount, loadCart, addItem, updateQuantity, removeItem, clear }
})
```

**책임**:
- 장바구니 아이템 관리
- 총 금액 계산
- LocalStorage 동기화

---

### Component 3.4: Order Store
**역할**: 주문 관리

**구현**:
```javascript
// stores/order.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'
import { useCartStore } from './cart'

export const useOrderStore = defineStore('order', () => {
  const orders = ref([])
  const loading = ref(false)
  const error = ref(null)

  const createOrder = async () => {
    const cartStore = useCartStore()
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/api/orders', {
        items: cartStore.items.map(item => ({
          menu_id: item.menuId,
          quantity: item.quantity
        })),
        total_amount: cartStore.totalAmount
      })
      cartStore.clear()
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const loadOrders = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/api/orders')
      orders.value = response.data
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  return { orders, loading, error, createOrder, loadOrders }
})
```

**책임**:
- 주문 생성
- 주문 내역 조회
- API 호출 및 에러 처리

---

## 4. API Communication Layer (API 통신 계층)

### Component 4.1: Axios Instance
**역할**: HTTP 클라이언트, API 호출 관리

**구현**: (nfr-design-patterns.md의 Pattern 2.3 참조)

**책임**:
- API 호출
- 세션 토큰 자동 추가
- 에러 처리 및 재시도
- 401 Unauthorized 처리

---

## 5. View Layer (뷰 계층)

### Component 5.1: LoginView
**역할**: 테이블 로그인 화면

**책임**:
- 로그인 폼 표시
- 입력 검증
- 로그인 API 호출
- 자동 로그인 처리

---

### Component 5.2: MenuView
**역할**: 메뉴 조회 및 탐색 화면

**책임**:
- 카테고리 탭 표시
- 메뉴 카드 렌더링
- 메뉴 상세 모달
- 장바구니 추가

**하위 컴포넌트**:
- CategoryTabs
- MenuCard
- MenuDetailModal

---

### Component 5.3: CartView
**역할**: 장바구니 관리 화면

**책임**:
- 장바구니 아이템 목록
- 수량 조절 (+/-)
- 아이템 삭제
- 총 금액 표시
- 주문 확정

**하위 컴포넌트**:
- CartItem
- CartSummary
- OrderConfirmModal

---

### Component 5.4: OrderHistoryView
**역할**: 주문 내역 조회 화면

**책임**:
- 주문 목록 표시
- 주문 상태 표시
- 주문 상세 모달

**하위 컴포넌트**:
- OrderCard
- OrderDetailModal

---

## 6. Shared Components (공통 컴포넌트)

### Component 6.1: AppHeader
**역할**: 앱 헤더, 네비게이션

**책임**:
- 매장/테이블 정보 표시
- 네비게이션 메뉴
- 장바구니 아이콘 + 배지

---

### Component 6.2: LoadingSpinner
**역할**: 로딩 인디케이터

**책임**:
- 로딩 중 스피너 표시
- 전체 화면 또는 인라인

---

### Component 6.3: ErrorMessage
**역할**: 에러 메시지 표시

**책임**:
- 에러 메시지 표시
- 재시도 버튼 (선택사항)

---

### Component 6.4: Toast
**역할**: 토스트 메시지 (nfr-design-patterns.md의 Pattern 4.1 참조)

**책임**:
- 성공/에러/정보 메시지 표시
- 자동 닫기 (2초)

---

## 7. Utility Layer (유틸리티 계층)

### Component 7.1: Composables
**역할**: 재사용 가능한 로직

**예시**:
```javascript
// composables/useToast.js
export const useToast = () => {
  const showToast = (message, type = 'info') => {
    // Toast 표시 로직
  }
  return { showToast }
}

// composables/useAuth.js
export const useAuth = () => {
  const authStore = useAuthStore()
  const isLoggedIn = computed(() => !!authStore.session)
  return { isLoggedIn }
}
```

---

## Logical Components Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Vue Application                     │
│                    (main.js)                         │
└──────────────────────┬──────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   ┌────────┐    ┌─────────┐   ┌──────────┐
   │ Pinia  │    │  Router │   │   App    │
   │ Stores │    │         │   │   Root   │
   └────┬───┘    └────┬────┘   └────┬─────┘
        │             │              │
        │             │              │
        ▼             ▼              ▼
   ┌─────────────────────────────────────┐
   │          View Components            │
   │  (Login, Menu, Cart, OrderHistory)  │
   └──────────────┬──────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │       Shared Components             │
   │  (Header, Loading, Error, Toast)    │
   └──────────────┬──────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │         API Layer (Axios)           │
   └──────────────┬──────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │       Backend API (FastAPI)         │
   └─────────────────────────────────────┘
```

---

## Component Summary

| 계층 | 컴포넌트 수 | 컴포넌트 |
|------|------------|----------|
| Application Core | 2 | Vue App, Root Component |
| Routing | 1 | Vue Router |
| State Management | 4 | Auth, Menu, Cart, Order Stores |
| API Communication | 1 | Axios Instance |
| View | 4 | Login, Menu, Cart, OrderHistory |
| Shared | 4 | Header, Loading, Error, Toast |
| Utility | 2+ | Composables |
| **총계** | **18+** | |

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
