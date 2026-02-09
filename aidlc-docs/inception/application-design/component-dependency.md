# Component Dependencies

## Dependency Overview

이 문서는 컴포넌트 간 의존성 관계와 통신 패턴을 정의합니다.

---

## Backend Component Dependencies

### Dependency Matrix

| Component | Depends On | Used By |
|-----------|------------|---------|
| **AuthController** | AuthService | - |
| **MenuController** | MenuService | - |
| **OrderController** | OrderService | - |
| **TableController** | TableService | - |
| **SSEController** | OrderService, SSEService | - |
| **AuthService** | UserRepository, TableRepository | AuthController |
| **MenuService** | MenuRepository | MenuController, OrderService |
| **OrderService** | OrderRepository, MenuRepository, SSEService | OrderController, SSEController |
| **TableService** | TableRepository, OrderRepository | TableController |
| **SSEService** | - | OrderService, SSEController |
| **UserRepository** | Database | AuthService |
| **TableRepository** | Database | AuthService, TableService |
| **MenuRepository** | Database | MenuService, OrderService |
| **OrderRepository** | Database | OrderService, TableService |

---

### Dependency Graph (Backend)

```
Controllers (API Layer)
├─ AuthController
│  └─ AuthService
│     ├─ UserRepository → Database
│     └─ TableRepository → Database
│
├─ MenuController
│  └─ MenuService
│     └─ MenuRepository → Database
│
├─ OrderController
│  └─ OrderService
│     ├─ OrderRepository → Database
│     ├─ MenuRepository → Database
│     └─ SSEService
│
├─ TableController
│  └─ TableService
│     ├─ TableRepository → Database
│     └─ OrderRepository → Database
│
└─ SSEController
   ├─ OrderService
   └─ SSEService
```

---

## Frontend Component Dependencies

### Customer App Dependencies

```
App (Root)
├─ AppHeader (Shared)
├─ Router
│  ├─ LoginView
│  │  └─ authStore
│  │
│  ├─ MenuView
│  │  ├─ menuStore
│  │  ├─ cartStore
│  │  ├─ CategoryTabs
│  │  ├─ MenuCard
│  │  └─ MenuDetail
│  │
│  ├─ CartView
│  │  ├─ cartStore
│  │  ├─ orderStore
│  │  ├─ CartItem
│  │  └─ CartSummary
│  │
│  └─ OrderHistoryView
│     ├─ orderStore
│     ├─ OrderCard
│     └─ OrderDetail
│
├─ LoadingSpinner (Shared)
└─ ErrorMessage (Shared)
```

---

### Admin App Dependencies

```
App (Root)
├─ AppHeader (Shared)
├─ Router
│  ├─ AdminLoginView
│  │  └─ adminAuthStore
│  │
│  ├─ OrderDashboardView
│  │  ├─ adminOrderStore
│  │  ├─ TableCard
│  │  ├─ OrderDetailModal
│  │  └─ SSEConnection
│  │
│  ├─ TableManagementView
│  │  ├─ adminTableStore
│  │  ├─ TableSetupModal
│  │  └─ OrderHistoryModal
│  │
│  └─ MenuManagementView
│     ├─ adminMenuStore
│     ├─ MenuForm
│     ├─ MenuList
│     └─ ImageUploader
│
├─ LoadingSpinner (Shared)
└─ ErrorMessage (Shared)
```

---

### Pinia Store Dependencies

```
Stores (State Management)
├─ authStore
│  └─ API: AuthController
│
├─ menuStore
│  └─ API: MenuController
│
├─ cartStore
│  ├─ LocalStorage
│  └─ menuStore (메뉴 정보 참조)
│
├─ orderStore
│  ├─ API: OrderController
│  └─ cartStore (주문 생성 시)
│
├─ adminAuthStore
│  └─ API: AuthController
│
├─ adminOrderStore
│  ├─ API: OrderController
│  └─ SSE: SSEController
│
├─ adminTableStore
│  └─ API: TableController
│
└─ adminMenuStore
   └─ API: MenuController
```

---

## Communication Patterns

### Pattern 1: RESTful API Communication

**Customer → Backend**
```
Vue Component → Pinia Store → Axios → FastAPI Controller → Service → Repository → Database
```

**Example: 주문 생성**
```
CartView.placeOrder()
  → orderStore.createOrder()
    → axios.post('/api/orders')
      → OrderController.create_order()
        → OrderService.create_order()
          → OrderRepository.create()
            → Database
```

---

### Pattern 2: Real-time Communication (SSE)

**Backend → Admin**
```
OrderService.create_order()
  → SSEService.broadcast()
    → SSE Stream
      → AdminApp EventSource
        → adminOrderStore.onNewOrder()
          → OrderDashboardView (UI Update)
```

**Example: 실시간 주문 알림**
```
1. Customer creates order
2. OrderService broadcasts event via SSE
3. Admin dashboard receives event
4. UI updates automatically
```

---

### Pattern 3: LocalStorage Sync

**Cart Management**
```
CartView (Add Item)
  → cartStore.addItem()
    → Update Pinia state
    → Sync to LocalStorage
      → localStorage.setItem('cart', JSON.stringify(cart))

Page Refresh
  → cartStore.init()
    → Load from LocalStorage
      → localStorage.getItem('cart')
    → Restore Pinia state
```

---

### Pattern 4: Authentication Flow

**Table Login**
```
LoginView.login()
  → authStore.login()
    → axios.post('/api/auth/table/login')
      → AuthController.table_login()
        → AuthService.authenticate_table()
          → TableRepository.get_by_table_number()
          → AuthService.create_jwt_token()
    → Save token to LocalStorage
    → Redirect to MenuView
```

**Admin Login**
```
AdminLoginView.login()
  → adminAuthStore.login()
    → axios.post('/api/auth/admin/login')
      → AuthController.admin_login()
        → AuthService.authenticate_admin()
          → UserRepository.get_by_username()
          → AuthService.verify_password()
          → AuthService.create_jwt_token()
    → Save token to LocalStorage
    → Redirect to OrderDashboardView
```

---

### Pattern 5: Middleware Authentication

**Protected API Requests**
```
Vue Component → Pinia Store → Axios (with JWT in header)
  → FastAPI Middleware
    → Verify JWT token
    → Extract user info
    → Pass to Controller
      → Controller (authenticated request)
```

**Middleware Flow**
```
Request
  → AuthMiddleware.verify_token()
    → Extract JWT from header
    → AuthService.verify_jwt_token()
    → Attach user to request
  → Controller (request.user available)
```

---

## Data Flow Diagrams

### Customer Order Flow

```
Customer (Browser)
  ↓
[MenuView] → menuStore → GET /api/menus → MenuController → MenuService → MenuRepository → Database
  ↓
[CartView] → cartStore (LocalStorage)
  ↓
[CartView] → orderStore → POST /api/orders → OrderController → OrderService
  ↓                                                                ↓
  ↓                                                         SSEService.broadcast()
  ↓                                                                ↓
[OrderHistoryView] ← orderStore ← GET /api/orders          Admin Dashboard (SSE)
```

---

### Admin Order Management Flow

```
Admin (Browser)
  ↓
[AdminLoginView] → adminAuthStore → POST /api/auth/admin/login → AuthController → AuthService
  ↓
[OrderDashboardView] → adminOrderStore
  ↓                          ↓
  ↓                    GET /api/admin/orders (initial load)
  ↓                          ↓
  ↓                    SSE /api/admin/orders/stream (real-time updates)
  ↓                          ↓
[Update Status] → PUT /api/admin/orders/{id}/status → OrderController → OrderService
                                                                            ↓
                                                                     SSEService.broadcast()
```

---

### Table Session Management Flow

```
Admin (Browser)
  ↓
[TableManagementView] → adminTableStore
  ↓
[Setup Table] → POST /api/admin/tables/setup → TableController → TableService → TableRepository
  ↓
[Complete Session] → POST /api/admin/tables/{id}/complete → TableController → TableService
                                                                                  ↓
                                                                         OrderRepository.move_to_history()
                                                                                  ↓
                                                                         TableRepository.update() (reset)
```

---

## Dependency Injection

### Backend (FastAPI)

**Service Injection**
```python
# Dependency function
def get_order_service(
    order_repo: OrderRepository = Depends(get_order_repository),
    menu_repo: MenuRepository = Depends(get_menu_repository),
    sse_service: SSEService = Depends(get_sse_service)
) -> OrderService:
    return OrderService(order_repo, menu_repo, sse_service)

# Controller
@router.post("/orders")
async def create_order(
    request: OrderCreateRequest,
    service: OrderService = Depends(get_order_service)
) -> OrderResponse:
    return await service.create_order(request)
```

---

### Frontend (Vue.js + Pinia)

**Store Injection**
```typescript
// Component
import { useOrderStore } from '@/stores/order'
import { useCartStore } from '@/stores/cart'

export default {
  setup() {
    const orderStore = useOrderStore()
    const cartStore = useCartStore()
    
    const placeOrder = async () => {
      const items = cartStore.items
      await orderStore.createOrder(items)
      cartStore.clear()
    }
    
    return { placeOrder }
  }
}
```

---

## Circular Dependency Prevention

**Rule**: Repository → Service → Controller (단방향)

**Avoided Pattern** (❌):
```
ServiceA → ServiceB → ServiceA (circular)
```

**Correct Pattern** (✅):
```
ServiceA → Repository
ServiceB → Repository
(Both services use same repository, no circular dependency)
```

---

## Dependency Summary

### Backend
- **Controllers**: 5개 (API 엔드포인트)
- **Services**: 5개 (비즈니스 로직)
- **Repositories**: 4개 (데이터 접근)
- **Total Dependencies**: 14개 주요 의존성

### Frontend
- **Views**: 8개 (Customer: 4, Admin: 4)
- **Stores**: 7개 (Pinia)
- **Shared Components**: 3개
- **Total Dependencies**: 18개 주요 의존성

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
