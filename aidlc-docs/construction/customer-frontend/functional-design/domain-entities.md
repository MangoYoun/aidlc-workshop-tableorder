# Domain Entities - Customer Frontend

## Overview

Customer Frontend의 도메인 엔티티는 클라이언트 측에서 관리되는 데이터 구조입니다. Backend API로부터 받은 데이터를 TypeScript 인터페이스(또는 JavaScript 객체)로 표현합니다.

---

## 1. TableSession (테이블 세션)

### 목적
현재 테이블의 로그인 세션 정보를 관리합니다.

### 속성

| 속성 | 타입 | 필수 | 설명 |
|------|------|------|------|
| storeId | number | ✅ | 매장 ID |
| storeName | string | ✅ | 매장 이름 (UI 표시용) |
| tableNumber | string | ✅ | 테이블 번호 (예: "T01") |
| tableName | string | ✅ | 테이블 이름 (UI 표시용) |
| sessionToken | string | ✅ | 세션 토큰 (API 인증용) |
| createdAt | string (ISO 8601) | ✅ | 세션 생성 시각 |
| expiresAt | string (ISO 8601) | ✅ | 세션 만료 시각 |

### 저장 위치
- **LocalStorage** (`table_session` 키)

### 생명주기
- **생성**: 테이블 로그인 성공 시
- **갱신**: 주문 생성 시 (last_order_at 업데이트)
- **삭제**: 세션 만료 또는 로그아웃 시

### 예시
```javascript
{
  storeId: 1,
  storeName: "맛있는 식당",
  tableNumber: "T01",
  tableName: "테이블 1",
  sessionToken: "abc123xyz789",
  createdAt: "2026-02-09T10:00:00Z",
  expiresAt: "2026-02-10T02:00:00Z"
}
```

---

## 2. Menu (메뉴)

### 목적
메뉴 정보를 표현합니다.

### 속성

| 속성 | 타입 | 필수 | 설명 |
|------|------|------|------|
| id | number | ✅ | 메뉴 ID |
| categoryId | number | ✅ | 카테고리 ID |
| categoryName | string | ✅ | 카테고리 이름 |
| name | string | ✅ | 메뉴명 |
| description | string | ❌ | 메뉴 설명 |
| price | number | ✅ | 가격 (원) |
| imageUrl | string | ❌ | 이미지 URL |
| isAvailable | boolean | ✅ | 판매 가능 여부 |
| displayOrder | number | ✅ | 노출 순서 |

### 저장 위치
- **Pinia Store** (`menuStore`)
- Backend API로부터 로드

### 생명주기
- **생성**: 메뉴 화면 진입 시 API 호출
- **갱신**: 메뉴 화면 새로고침 시
- **삭제**: 앱 종료 시 (메모리에서만 존재)

### 예시
```javascript
{
  id: 1,
  categoryId: 1,
  categoryName: "메인 요리",
  name: "김치찌개",
  description: "얼큰한 김치찌개",
  price: 8000,
  imageUrl: "https://example.com/images/kimchi-jjigae.jpg",
  isAvailable: true,
  displayOrder: 1
}
```

---

## 3. Category (카테고리)

### 목적
메뉴 카테고리 정보를 표현합니다.

### 속성

| 속성 | 타입 | 필수 | 설명 |
|------|------|------|------|
| id | number | ✅ | 카테고리 ID |
| name | string | ✅ | 카테고리 이름 |
| displayOrder | number | ✅ | 노출 순서 |

### 저장 위치
- **Pinia Store** (`menuStore`)
- Backend API로부터 로드

### 생명주기
- **생성**: 메뉴 화면 진입 시 API 호출
- **갱신**: 메뉴 화면 새로고침 시
- **삭제**: 앱 종료 시

### 예시
```javascript
{
  id: 1,
  name: "메인 요리",
  displayOrder: 1
}
```

---

## 4. CartItem (장바구니 아이템)

### 목적
장바구니에 담긴 메뉴 아이템을 표현합니다.

### 속성

| 속성 | 타입 | 필수 | 설명 |
|------|------|------|------|
| menuId | number | ✅ | 메뉴 ID |
| menuName | string | ✅ | 메뉴명 (UI 표시용) |
| price | number | ✅ | 단가 (원) |
| quantity | number | ✅ | 수량 |
| subtotal | number | ✅ | 소계 (price × quantity) |
| imageUrl | string | ❌ | 이미지 URL |

### 저장 위치
- **Pinia Store** (`cartStore`)
- **LocalStorage** (`cart_items` 키)

### 생명주기
- **생성**: 메뉴 선택 시
- **갱신**: 수량 증가/감소 시
- **삭제**: 아이템 삭제 또는 주문 완료 시

### 비즈니스 규칙
- 수량은 최소 1개 이상
- 수량 0이 되면 자동 삭제
- 동일 메뉴 추가 시 수량만 증가

### 예시
```javascript
{
  menuId: 1,
  menuName: "김치찌개",
  price: 8000,
  quantity: 2,
  subtotal: 16000,
  imageUrl: "https://example.com/images/kimchi-jjigae.jpg"
}
```

---

## 5. Cart (장바구니)

### 목적
장바구니 전체 정보를 관리합니다.

### 속성

| 속성 | 타입 | 필수 | 설명 |
|------|------|------|------|
| items | CartItem[] | ✅ | 장바구니 아이템 목록 |
| totalAmount | number | ✅ | 총 금액 (원) |
| itemCount | number | ✅ | 총 아이템 수 |

### 저장 위치
- **Pinia Store** (`cartStore`)
- **LocalStorage** (`cart_items` 키)

### 생명주기
- **생성**: 앱 시작 시 (LocalStorage에서 복원)
- **갱신**: 장바구니 아이템 변경 시
- **삭제**: 주문 완료 또는 세션 종료 시

### 계산 로직
```javascript
totalAmount = items.reduce((sum, item) => sum + item.subtotal, 0)
itemCount = items.reduce((sum, item) => sum + item.quantity, 0)
```

### 예시
```javascript
{
  items: [
    { menuId: 1, menuName: "김치찌개", price: 8000, quantity: 2, subtotal: 16000 },
    { menuId: 2, menuName: "된장찌개", price: 7000, quantity: 1, subtotal: 7000 }
  ],
  totalAmount: 23000,
  itemCount: 3
}
```

---

## 6. Order (주문)

### 목적
주문 정보를 표현합니다.

### 속성

| 속성 | 타입 | 필수 | 설명 |
|------|------|------|------|
| id | number | ✅ | 주문 ID |
| orderNumber | string | ✅ | 주문 번호 (예: "ORD-20260209-001") |
| storeId | number | ✅ | 매장 ID |
| tableNumber | string | ✅ | 테이블 번호 |
| sessionId | number | ✅ | 세션 ID |
| items | OrderItem[] | ✅ | 주문 아이템 목록 |
| totalAmount | number | ✅ | 총 금액 (원) |
| status | OrderStatus | ✅ | 주문 상태 |
| createdAt | string (ISO 8601) | ✅ | 주문 생성 시각 |

### OrderStatus (주문 상태)
```typescript
enum OrderStatus {
  PENDING = "대기중",
  PREPARING = "준비중",
  COMPLETED = "완료"
}
```

### 저장 위치
- **Pinia Store** (`orderStore`)
- Backend API로부터 로드

### 생명주기
- **생성**: 주문 생성 API 호출 성공 시
- **갱신**: 주문 내역 조회 시
- **삭제**: 세션 종료 시

### 예시
```javascript
{
  id: 1,
  orderNumber: "ORD-20260209-001",
  storeId: 1,
  tableNumber: "T01",
  sessionId: 123,
  items: [
    { menuId: 1, menuName: "김치찌개", price: 8000, quantity: 2 }
  ],
  totalAmount: 16000,
  status: "대기중",
  createdAt: "2026-02-09T10:30:00Z"
}
```

---

## 7. OrderItem (주문 아이템)

### 목적
주문에 포함된 개별 메뉴 아이템을 표현합니다.

### 속성

| 속성 | 타입 | 필수 | 설명 |
|------|------|------|------|
| menuId | number | ✅ | 메뉴 ID |
| menuName | string | ✅ | 메뉴명 (주문 시점 스냅샷) |
| price | number | ✅ | 단가 (주문 시점 스냅샷) |
| quantity | number | ✅ | 수량 |

### 저장 위치
- **Order 엔티티 내부**

### 비즈니스 규칙
- 주문 시점의 메뉴명과 가격을 스냅샷으로 저장
- 이후 메뉴 정보 변경에 영향받지 않음

### 예시
```javascript
{
  menuId: 1,
  menuName: "김치찌개",
  price: 8000,
  quantity: 2
}
```

---

## Entity Relationships

```
TableSession (1) ─────────────────┐
                                  │
                                  ▼
                            Order (N)
                                  │
                                  ├─ OrderItem (N)
                                  │
Menu (N) ─────────────────────────┘
    │
    └─ Category (1)

Cart (1) ─── CartItem (N) ─── Menu (1)
```

### 관계 설명

1. **TableSession → Order**: 1:N
   - 하나의 테이블 세션에 여러 주문 가능

2. **Order → OrderItem**: 1:N
   - 하나의 주문에 여러 아이템 포함

3. **Menu → Category**: N:1
   - 여러 메뉴가 하나의 카테고리에 속함

4. **Cart → CartItem**: 1:N
   - 하나의 장바구니에 여러 아이템 포함

5. **CartItem → Menu**: N:1
   - 장바구니 아이템은 메뉴 정보 참조

---

## Data Flow

### 1. 로그인 플로우
```
Backend API → TableSession → LocalStorage
```

### 2. 메뉴 조회 플로우
```
Backend API → Menu[] + Category[] → Pinia Store (menuStore)
```

### 3. 장바구니 플로우
```
Menu → CartItem → Cart → LocalStorage
```

### 4. 주문 생성 플로우
```
Cart → Backend API → Order → Pinia Store (orderStore)
```

### 5. 주문 내역 조회 플로우
```
Backend API → Order[] → Pinia Store (orderStore)
```

---

## LocalStorage Schema

### table_session
```json
{
  "storeId": 1,
  "storeName": "맛있는 식당",
  "tableNumber": "T01",
  "tableName": "테이블 1",
  "sessionToken": "abc123xyz789",
  "createdAt": "2026-02-09T10:00:00Z",
  "expiresAt": "2026-02-10T02:00:00Z"
}
```

### cart_items
```json
[
  {
    "menuId": 1,
    "menuName": "김치찌개",
    "price": 8000,
    "quantity": 2,
    "subtotal": 16000,
    "imageUrl": "https://example.com/images/kimchi-jjigae.jpg"
  }
]
```

---

## Validation Rules

### TableSession
- `sessionToken`은 비어있으면 안 됨
- `expiresAt`은 현재 시각보다 미래여야 함

### Menu
- `price`는 0보다 커야 함
- `name`은 비어있으면 안 됨

### CartItem
- `quantity`는 1 이상이어야 함
- `price`는 0보다 커야 함

### Order
- `items`는 최소 1개 이상이어야 함
- `totalAmount`는 0보다 커야 함

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
