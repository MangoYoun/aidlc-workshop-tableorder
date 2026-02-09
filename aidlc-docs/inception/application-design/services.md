# Service Layer Design

## Service Layer 개요

Service Layer는 **Rich Services** 패턴을 따르며, 비즈니스 로직을 포함합니다.

**설계 원칙:**
- Controller는 얇게 유지 (요청/응답 처리만)
- Service에 비즈니스 로직 집중
- Repository를 통한 데이터 접근
- 트랜잭션 관리

---

## Backend Services

### 1. AuthService

**책임**: 인증 및 권한 관리

**주요 기능:**
- 테이블 로그인 검증
- 관리자 로그인 검증
- JWT 토큰 생성 및 검증
- 비밀번호 해싱 및 검증 (bcrypt)
- 세션 관리

**의존성:**
- UserRepository
- TableRepository

**Orchestration 패턴:**
```
Login Request → AuthService.authenticate()
  ├─ Repository.get_user()
  ├─ verify_password()
  ├─ create_jwt_token()
  └─ Return token
```

---

### 2. MenuService

**책임**: 메뉴 관리

**주요 기능:**
- 메뉴 CRUD
- 메뉴 검증
- 이미지 업로드 처리
- 메뉴 순서 조정

**의존성:**
- MenuRepository

**Orchestration 패턴:**
```
Create Menu Request → MenuService.create_menu()
  ├─ Validate menu data
  ├─ Upload image (if provided)
  ├─ Repository.create()
  └─ Return menu
```

---

### 3. OrderService

**책임**: 주문 관리

**주요 기능:**
- 주문 생성 및 검증
- 주문 상태 관리
- 주문 금액 계산
- 실시간 주문 알림 (SSE)

**의존성:**
- OrderRepository
- MenuRepository
- SSEService

**Orchestration 패턴:**
```
Create Order Request → OrderService.create_order()
  ├─ Validate order items
  ├─ MenuRepository.get_menus() (가격 확인)
  ├─ Calculate total amount
  ├─ OrderRepository.create()
  ├─ SSEService.broadcast() (실시간 알림)
  └─ Return order
```

---

### 4. TableService

**책임**: 테이블 및 세션 관리

**주요 기능:**
- 테이블 초기 설정
- 테이블 세션 관리
- 세션 만료 처리
- 과거 주문 이력 관리

**의존성:**
- TableRepository
- OrderRepository

**Orchestration 패턴:**
```
Complete Session Request → TableService.complete_table_session()
  ├─ TableRepository.get_by_id()
  ├─ OrderRepository.get_by_session()
  ├─ OrderRepository.move_to_history()
  ├─ TableRepository.update() (리셋)
  └─ Return success
```

---

### 5. SSEService

**책임**: 실시간 통신 관리

**주요 기능:**
- SSE 연결 관리
- 클라이언트 연결 추적
- 이벤트 브로드캐스트

**의존성:**
- None (독립적)

**Orchestration 패턴:**
```
New Order Event → SSEService.broadcast()
  ├─ Get all connected clients
  ├─ Format event data
  ├─ Send to each client queue
  └─ Return
```

---

## Frontend Services (Pinia Stores)

### 1. authStore

**책임**: 인증 상태 관리

**주요 기능:**
- 로그인 상태 관리
- 토큰 저장/로드
- 자동 로그인

**State:**
```typescript
{
  isAuthenticated: boolean
  token: string | null
  user: User | null
}
```

---

### 2. menuStore

**책임**: 메뉴 데이터 관리

**주요 기능:**
- 메뉴 목록 캐싱
- 카테고리별 필터링

**State:**
```typescript
{
  menus: Menu[]
  categories: Category[]
  selectedCategory: string | null
}
```

---

### 3. cartStore

**책임**: 장바구니 상태 관리

**주요 기능:**
- 장바구니 아이템 관리
- LocalStorage 동기화
- 총 금액 계산

**State:**
```typescript
{
  items: CartItem[]
  total: number
}
```

---

### 4. orderStore

**책임**: 주문 데이터 관리

**주요 기능:**
- 주문 내역 캐싱
- 주문 생성

**State:**
```typescript
{
  orders: Order[]
  currentOrder: Order | null
}
```

---

### 5. adminOrderStore

**책임**: 관리자 주문 관리

**주요 기능:**
- 실시간 주문 업데이트
- SSE 연결 관리
- 주문 상태 변경

**State:**
```typescript
{
  orders: Order[]
  sseConnection: EventSource | null
}
```

---

### 6. adminTableStore

**책임**: 테이블 관리

**주요 기능:**
- 테이블 목록 관리
- 테이블 세션 관리

**State:**
```typescript
{
  tables: Table[]
  selectedTable: Table | null
}
```

---

### 7. adminMenuStore

**책임**: 메뉴 관리 (관리자)

**주요 기능:**
- 메뉴 CRUD
- 이미지 업로드

**State:**
```typescript
{
  menus: Menu[]
  categories: Category[]
}
```

---

## Service Interaction Patterns

### Pattern 1: Simple CRUD
```
Controller → Service → Repository → Database
```

### Pattern 2: Complex Business Logic
```
Controller → Service
  ├─ Repository A (read)
  ├─ Business Logic
  ├─ Repository B (write)
  └─ External Service (SSE)
```

### Pattern 3: Transaction Management
```
Controller → Service (begin transaction)
  ├─ Repository A (write)
  ├─ Repository B (write)
  ├─ Commit or Rollback
  └─ Return result
```

---

## Error Handling in Services

**Strategy**: Hybrid (Centralized + Local)

**Service-level Error Handling:**
```python
class OrderService:
    async def create_order(self, order_data: OrderCreateDto) -> Order:
        try:
            # Business logic
            order = await self.order_repository.create(order_data)
            await self.sse_service.broadcast("new_order", order.dict())
            return order
        except ValidationError as e:
            # Local handling: 비즈니스 검증 에러
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            # Propagate to centralized handler
            raise
```

**Centralized Error Handler** (FastAPI):
```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log error
    logger.error(f"Unhandled exception: {exc}")
    # Return standardized error response
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
```

---

## Service Summary

**Backend Services**: 5개
- AuthService
- MenuService
- OrderService
- TableService
- SSEService

**Frontend Stores (Pinia)**: 7개
- authStore
- menuStore
- cartStore
- orderStore
- adminOrderStore
- adminTableStore
- adminMenuStore

**총 Services**: 12개

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
