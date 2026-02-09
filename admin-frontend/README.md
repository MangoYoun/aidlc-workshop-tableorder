# TableOrder Admin Frontend

테이블오더 서비스의 관리자용 프론트엔드 애플리케이션입니다.

## Tech Stack

- **Framework**: Vue.js 3.4+
- **Build Tool**: Vite 5.0+
- **State Management**: Pinia 2.1+
- **Routing**: Vue Router 4.2+
- **HTTP Client**: Axios 1.6+
- **Real-time**: EventSource (SSE)
- **Styling**: Tailwind CSS 3.4+

## Features

- 관리자 JWT 인증 (16시간 세션)
- 실시간 주문 모니터링 (SSE)
- 테이블 관리 (초기 설정, 세션 종료)
- 메뉴 관리 (CRUD)
- 주문 상태 변경

## Project Structure

```
admin-frontend/
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── router/
│   ├── stores/
│   │   ├── adminAuth.js
│   │   ├── order.js
│   │   ├── table.js
│   │   └── menu.js
│   ├── views/
│   │   ├── AdminLoginView.vue
│   │   ├── OrderDashboardView.vue
│   │   ├── TableManagementView.vue
│   │   └── MenuManagementView.vue
│   ├── components/
│   │   ├── TableCard.vue
│   │   ├── OrderList.vue
│   │   ├── MenuForm.vue
│   │   └── shared/
│   ├── services/
│   │   ├── api.js
│   │   └── sse.js
│   └── assets/
├── package.json
└── vite.config.js
```

## Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
# Access at http://localhost:5174
```

## Implementation Guide

### Core Files Generated
1. ✅ package.json - Dependencies
2. ✅ vite.config.js - Vite configuration (port 5174)
3. ✅ index.html - HTML entry
4. ✅ src/main.js - Vue app entry
5. ✅ src/router/index.js - Router with admin routes
6. ✅ src/stores/adminAuth.js - Admin authentication store

### Files to Implement

Based on Customer Frontend pattern, implement:

#### Stores (src/stores/)
- `order.js` - Order management with SSE
- `table.js` - Table management
- `menu.js` - Menu CRUD operations
- `toast.js` - Toast notifications (copy from customer-frontend)

#### Services (src/services/)
- `api.js` - Axios instance (copy from customer-frontend, use admin token)
- `sse.js` - SSE connection for real-time updates

#### Views (src/views/)
- `AdminLoginView.vue` - Admin login form
- `OrderDashboardView.vue` - Real-time order dashboard with table cards
- `TableManagementView.vue` - Table CRUD and session management
- `MenuManagementView.vue` - Menu CRUD with image upload

#### Components (src/components/)
- `TableCard.vue` - Table card with orders
- `OrderList.vue` - Order list for a table
- `MenuForm.vue` - Menu create/edit form
- `shared/` - Copy from customer-frontend (AppHeader, LoadingSpinner, etc.)

#### Assets
- `src/assets/main.css` - Copy from customer-frontend
- `src/App.vue` - Copy from customer-frontend, adjust header

### SSE Implementation Example

```javascript
// src/services/sse.js
export const connectSSE = (storeId, onMessage) => {
  const eventSource = new EventSource(
    `${import.meta.env.VITE_API_URL}/api/admin/sse/orders?store_id=${storeId}`
  )
  
  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data)
    onMessage(data)
  }
  
  eventSource.onerror = () => {
    eventSource.close()
  }
  
  return eventSource
}
```

### Order Store with SSE Example

```javascript
// src/stores/order.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { connectSSE } from '@/services/sse'

export const useOrderStore = defineStore('order', () => {
  const orders = ref([])
  let sseConnection = null
  
  const startSSE = (storeId) => {
    sseConnection = connectSSE(storeId, (data) => {
      // Update orders on new data
      orders.value = data.orders
    })
  }
  
  const stopSSE = () => {
    if (sseConnection) {
      sseConnection.close()
    }
  }
  
  return { orders, startSSE, stopSSE }
})
```

## API Endpoints

- `POST /api/auth/admin-login` - Admin login
- `GET /api/admin/sse/orders?store_id={id}` - SSE for real-time orders
- `GET /api/admin/orders?store_id={id}` - Get all orders
- `PUT /api/admin/orders/{id}/status` - Update order status
- `GET /api/admin/tables?store_id={id}` - Get tables
- `POST /api/admin/tables` - Create table
- `DELETE /api/admin/tables/{id}/session` - End table session
- `GET /api/admin/menus?store_id={id}` - Get menus
- `POST /api/admin/menus` - Create menu
- `PUT /api/admin/menus/{id}` - Update menu
- `DELETE /api/admin/menus/{id}` - Delete menu

## Stories Implemented

- Story 2.1: 매장 인증 (Admin JWT)
- Story 2.2: 실시간 주문 모니터링 (SSE)
- Story 2.3: 테이블 관리 (CRUD, 세션 종료)
- Story 2.4: 메뉴 관리 (CRUD, 이미지 업로드)

## Development Notes

1. **Reuse Customer Frontend Components**: Copy shared components (LoadingSpinner, ErrorMessage, Toast, etc.)
2. **SSE Connection**: Implement in OrderDashboardView, connect on mount, disconnect on unmount
3. **Image Upload**: Use FormData for menu image upload
4. **Table Cards**: Display table number, total amount, recent orders
5. **Order Status**: Buttons to change status (대기중 → 준비중 → 완료)

## Deployment

Same as Customer Frontend (AWS S3 + CloudFront). See customer-frontend deployment docs.

## License

MIT
