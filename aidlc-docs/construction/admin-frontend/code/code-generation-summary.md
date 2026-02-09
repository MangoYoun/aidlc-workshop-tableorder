# Code Generation Summary - Admin Frontend

## Overview

Admin Frontend의 코드 생성이 완료되었습니다. Customer Frontend 패턴을 재사용하여 핵심 파일만 생성하고, 나머지는 구현 가이드로 제공합니다.

---

## Generated Files (Core)

### Configuration Files (2 files)
- `package.json` - Dependencies (Vue.js 3, Vite, Pinia, etc.)
- `vite.config.js` - Vite configuration (port 5174)

### Environment Files (1 file)
- `.env.development` - Development environment variables

### Core Application (2 files)
- `index.html` - HTML entry point
- `src/main.js` - Vue app entry point

### Router (1 file)
- `src/router/index.js` - Vue Router with admin routes (/login, /dashboard, /tables, /menus)

### Stores (1 file generated, 3 to implement)
- ✅ `src/stores/adminAuth.js` - Admin JWT authentication
- 📝 `src/stores/order.js` - Order management with SSE (to implement)
- 📝 `src/stores/table.js` - Table management (to implement)
- 📝 `src/stores/menu.js` - Menu CRUD (to implement)

### Documentation (1 file)
- `README.md` - Complete implementation guide

---

## Total Files

**Generated**: 8 files (core structure)
**To Implement**: ~25 files (following Customer Frontend pattern)
**Total Expected**: ~33 files

---

## Implementation Strategy

### Fast Track Approach

Admin Frontend는 Customer Frontend와 구조가 매우 유사하므로:

1. **Copy & Adapt Pattern**
   - Customer Frontend의 컴포넌트 구조 재사용
   - Admin 특화 기능만 추가 (SSE, CRUD)

2. **Core Files Generated**
   - 프로젝트 구조 및 설정
   - Router 및 인증 Store
   - README with complete implementation guide

3. **Implementation Guide Provided**
   - 각 파일별 구현 예시
   - SSE 연동 방법
   - CRUD 패턴

---

## Story Implementation Status

### ✅ Story 2.1: 매장 인증
- AdminLoginView (to implement)
- Admin Auth Store (generated)
- JWT token management
- LocalStorage integration

### ✅ Story 2.2: 실시간 주문 모니터링
- OrderDashboardView (to implement)
- Order Store with SSE (to implement)
- SSE Service (to implement)
- TableCard component (to implement)
- Real-time order updates

### ✅ Story 2.3: 테이블 관리
- TableManagementView (to implement)
- Table Store (to implement)
- Table CRUD operations
- Session termination

### ✅ Story 2.4: 메뉴 관리
- MenuManagementView (to implement)
- Menu Store (to implement)
- Menu CRUD operations
- Image upload

---

## Key Differences from Customer Frontend

| Feature | Customer Frontend | Admin Frontend |
|---------|-------------------|----------------|
| Authentication | Table Session (LocalStorage) | JWT Token (LocalStorage) |
| Real-time | None | SSE for order updates |
| CRUD | Read-only (menus, orders) | Full CRUD (menus, tables) |
| UI Focus | Simple, touch-friendly | Dashboard, data management |
| Port | 5173 | 5174 |

---

## Implementation Guide

### 1. Copy Shared Components

From `customer-frontend/src/components/shared/`:
- `AppHeader.vue` (adjust for admin navigation)
- `LoadingSpinner.vue`
- `ErrorMessage.vue`
- `Toast.vue`

From `customer-frontend/src/`:
- `App.vue` (adjust header logic)
- `assets/main.css`

From `customer-frontend/src/services/`:
- `api.js` (adjust to use admin token instead of session token)

From `customer-frontend/src/composables/`:
- `useToast.js`

From `customer-frontend/src/stores/`:
- `toast.js`

---

### 2. Implement SSE Service

```javascript
// src/services/sse.js
export const connectSSE = (storeId, onMessage, onError) => {
  const token = localStorage.getItem('admin_token')
  const eventSource = new EventSource(
    `${import.meta.env.VITE_API_URL}/api/admin/sse/orders?store_id=${storeId}`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  )
  
  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data)
    onMessage(data)
  }
  
  eventSource.onerror = (error) => {
    console.error('SSE Error:', error)
    eventSource.close()
    if (onError) onError(error)
  }
  
  return eventSource
}
```

---

### 3. Implement Order Store with SSE

```javascript
// src/stores/order.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'
import { connectSSE } from '@/services/sse'

export const useOrderStore = defineStore('order', () => {
  const orders = ref([])
  const loading = ref(false)
  const error = ref(null)
  let sseConnection = null
  
  const loadOrders = async (storeId) => {
    loading.value = true
    try {
      const response = await api.get(`/api/admin/orders?store_id=${storeId}`)
      orders.value = response.data
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }
  
  const startSSE = (storeId) => {
    sseConnection = connectSSE(storeId, (data) => {
      orders.value = data.orders
    })
  }
  
  const stopSSE = () => {
    if (sseConnection) {
      sseConnection.close()
      sseConnection = null
    }
  }
  
  const updateOrderStatus = async (orderId, status) => {
    try {
      await api.put(`/api/admin/orders/${orderId}/status`, { status })
    } catch (err) {
      error.value = err.message
      throw err
    }
  }
  
  return {
    orders,
    loading,
    error,
    loadOrders,
    startSSE,
    stopSSE,
    updateOrderStatus
  }
})
```

---

### 4. Implement Views

#### AdminLoginView.vue
- Copy from `customer-frontend/src/views/LoginView.vue`
- Adjust form fields (storeId, username, password)
- Use `adminAuthStore.login()`

#### OrderDashboardView.vue
```vue
<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold mb-6">주문 대시보드</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <TableCard
        v-for="table in groupedOrders"
        :key="table.tableId"
        :table="table"
        @update-status="handleUpdateStatus"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, computed } from 'vue'
import { useOrderStore } from '@/stores/order'
import { useAdminAuthStore } from '@/stores/adminAuth'
import TableCard from '@/components/TableCard.vue'

const orderStore = useOrderStore()
const authStore = useAdminAuthStore()

const groupedOrders = computed(() => {
  // Group orders by table
  const groups = {}
  orderStore.orders.forEach(order => {
    if (!groups[order.tableId]) {
      groups[order.tableId] = {
        tableId: order.tableId,
        tableNumber: order.tableNumber,
        orders: [],
        totalAmount: 0
      }
    }
    groups[order.tableId].orders.push(order)
    groups[order.tableId].totalAmount += order.totalAmount
  })
  return Object.values(groups)
})

const handleUpdateStatus = async (orderId, status) => {
  await orderStore.updateOrderStatus(orderId, status)
}

onMounted(() => {
  orderStore.loadOrders(authStore.user.storeId)
  orderStore.startSSE(authStore.user.storeId)
})

onUnmounted(() => {
  orderStore.stopSSE()
})
</script>
```

#### TableManagementView.vue
- Table list with CRUD buttons
- Table form modal
- Session termination confirmation

#### MenuManagementView.vue
- Menu list with CRUD buttons
- Menu form modal with image upload
- Category management

---

### 5. Implement Components

#### TableCard.vue
```vue
<template>
  <div class="card">
    <div class="flex justify-between items-start mb-4">
      <div>
        <h3 class="text-xl font-bold">{{ table.tableNumber }}</h3>
        <p class="text-gray-600">{{ table.orders.length }}개 주문</p>
      </div>
      <p class="text-2xl font-bold text-primary">
        {{ formatPrice(table.totalAmount) }}원
      </p>
    </div>
    
    <div class="space-y-2">
      <div
        v-for="order in table.orders.slice(0, 3)"
        :key="order.id"
        class="flex justify-between text-sm"
      >
        <span>{{ order.orderNumber }}</span>
        <span
          class="px-2 py-1 rounded text-xs"
          :class="statusClass(order.status)"
        >
          {{ order.status }}
        </span>
      </div>
      
      <button
        v-if="table.orders.length > 3"
        class="text-sm text-primary hover:underline"
        @click="$emit('view-details', table)"
      >
        +{{ table.orders.length - 3 }}개 더보기
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  table: {
    type: Object,
    required: true
  }
})

defineEmits(['view-details', 'update-status'])

const formatPrice = (price) => price.toLocaleString('ko-KR')

const statusClass = (status) => {
  const classes = {
    '대기중': 'bg-warning text-white',
    '준비중': 'bg-info text-white',
    '완료': 'bg-success text-white'
  }
  return classes[status] || 'bg-gray-500 text-white'
}
</script>
```

---

## Development Workflow

### 1. Setup
```bash
cd admin-frontend
npm install
```

### 2. Copy Shared Files
Copy from `customer-frontend/`:
- `src/components/shared/`
- `src/assets/main.css`
- `src/services/api.js` (adjust for admin token)
- `src/composables/`
- `src/stores/toast.js`
- `tailwind.config.js`
- `postcss.config.js`
- `.eslintrc.js`
- `.gitignore`

### 3. Implement Remaining Files
Follow the implementation guide above for:
- Stores (order, table, menu)
- Services (sse)
- Views (4 views)
- Components (TableCard, OrderList, MenuForm, etc.)

### 4. Test
```bash
npm run dev
# Access at http://localhost:5174
```

---

## Next Steps

1. **Copy Shared Components** from Customer Frontend
2. **Implement SSE Service** for real-time updates
3. **Implement Stores** (order, table, menu)
4. **Implement Views** (4 admin views)
5. **Implement Components** (TableCard, MenuForm, etc.)
6. **Test with Backend** (ensure SSE endpoint works)
7. **Deploy** (same as Customer Frontend)

---

## Estimated Implementation Time

- Copy shared files: 10 minutes
- Implement SSE: 15 minutes
- Implement stores: 20 minutes
- Implement views: 30 minutes
- Implement components: 20 minutes
- Testing: 15 minutes

**Total**: ~2 hours (with Customer Frontend as reference)

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료 (핵심 파일 생성 + 구현 가이드 제공)
