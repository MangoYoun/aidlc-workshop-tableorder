# Unit of Work Dependencies

## Dependency Matrix

| Unit | Backend Service | Customer Frontend | Admin Frontend |
|------|----------------|-------------------|----------------|
| **Backend Service** | - | Provides API | Provides API + SSE |
| **Customer Frontend** | Consumes API | - | None |
| **Admin Frontend** | Consumes API + SSE | None | - |

**Legend**:
- **Provides**: Unit가 다른 Unit에게 제공하는 서비스
- **Consumes**: Unit가 다른 Unit의 서비스를 사용
- **None**: 의존성 없음

---

## Dependency Details

### Backend Service
**Depends on**: None (독립적)

**Provides to**:
- **Customer Frontend**: RESTful API
  - 인증 API (테이블 로그인)
  - 메뉴 조회 API
  - 주문 생성 API
  - 주문 내역 조회 API
- **Admin Frontend**: RESTful API + SSE
  - 관리자 인증 API
  - 주문 관리 API
  - 테이블 관리 API
  - 메뉴 관리 API
  - 실시간 주문 업데이트 (SSE)

**Communication Pattern**: HTTP REST + Server-Sent Events (SSE)

---

### Customer Frontend
**Depends on**: Backend Service (API)

**Consumes from Backend**:
- POST `/api/auth/table-login` - 테이블 자동 로그인
- GET `/api/menus` - 메뉴 목록 조회
- GET `/api/menus/{id}` - 메뉴 상세 조회
- POST `/api/orders` - 주문 생성
- GET `/api/orders` - 주문 내역 조회 (현재 세션)

**Provides to**: None

**Communication Pattern**: HTTP REST (Axios)

**Data Flow**:
1. 테이블 로그인 → JWT 토큰 수신 → LocalStorage 저장
2. 메뉴 조회 → 메뉴 데이터 수신 → Pinia Store 저장
3. 장바구니 관리 → LocalStorage에 저장 (Backend 통신 없음)
4. 주문 생성 → 주문 데이터 전송 → 주문 번호 수신
5. 주문 내역 조회 → 주문 목록 수신 → 화면 표시

---

### Admin Frontend
**Depends on**: Backend Service (API + SSE)

**Consumes from Backend**:
- POST `/api/auth/admin-login` - 관리자 로그인
- GET `/api/admin/orders` - 주문 목록 조회
- PATCH `/api/admin/orders/{id}/status` - 주문 상태 변경
- DELETE `/api/admin/orders/{id}` - 주문 삭제
- POST `/api/admin/tables/init` - 테이블 초기 설정
- POST `/api/admin/tables/{id}/close-session` - 테이블 세션 종료
- GET `/api/admin/tables/history` - 과거 주문 내역 조회
- GET `/api/admin/menus` - 메뉴 목록 조회
- POST `/api/admin/menus` - 메뉴 등록
- PATCH `/api/admin/menus/{id}` - 메뉴 수정
- DELETE `/api/admin/menus/{id}` - 메뉴 삭제
- GET `/api/admin/sse/orders` - 실시간 주문 업데이트 (SSE)

**Provides to**: None

**Communication Pattern**: HTTP REST (Axios) + Server-Sent Events (EventSource)

**Data Flow**:
1. 관리자 로그인 → JWT 토큰 수신 → LocalStorage 저장
2. SSE 연결 → 실시간 주문 업데이트 수신 → Pinia Store 업데이트
3. 주문 상태 변경 → Backend 전송 → 성공 응답 수신
4. 테이블 관리 → Backend 전송 → 성공 응답 수신
5. 메뉴 관리 → Backend 전송 → 성공 응답 수신

---

## Communication Patterns

### 1. RESTful API (HTTP)
**Used by**: Customer Frontend, Admin Frontend

**Protocol**: HTTP/HTTPS  
**Format**: JSON  
**Authentication**: JWT (Bearer Token)

**Request Flow**:
```
Frontend → HTTP Request (with JWT) → Backend
Backend → Process Request → Database
Backend → HTTP Response (JSON) → Frontend
```

**Error Handling**:
- 4xx: Client errors (validation, authentication)
- 5xx: Server errors (database, internal)
- Frontend displays user-friendly error messages

---

### 2. Server-Sent Events (SSE)
**Used by**: Admin Frontend only

**Protocol**: HTTP (long-lived connection)  
**Format**: Event Stream  
**Authentication**: JWT (query parameter or header)

**Event Flow**:
```
Admin Frontend → SSE Connection → Backend
Backend → New Order Created → Emit Event
Admin Frontend → Receive Event → Update UI
```

**Event Types**:
- `order-created`: 새 주문 생성
- `order-updated`: 주문 상태 변경
- `order-deleted`: 주문 삭제

**Reconnection Strategy**:
- Auto-reconnect on connection loss
- Exponential backoff (1s, 2s, 4s, 8s, max 30s)

---

## Data Sharing Strategy

### Shared Data Models
**Strategy**: Duplicate (각 Unit에 복사)

**Backend (Python Pydantic)**:
```python
# backend/app/schemas/menu.py
class MenuResponse(BaseModel):
    id: int
    name: str
    price: int
    description: str
    category: str
    image_url: str
```

**Frontend (TypeScript Interface)**:
```typescript
// customer-frontend/src/types/menu.ts
interface Menu {
  id: number;
  name: string;
  price: number;
  description: string;
  category: string;
  imageUrl: string;
}
```

**Synchronization**: Manual (Backend 스키마 변경 시 Frontend 타입 수동 업데이트)

---

### Shared Constants
**Strategy**: Duplicate (각 Unit에 복사)

**Backend**:
```python
# backend/app/config.py
SESSION_TIMEOUT_HOURS = 16
ORDER_TIMEOUT_HOURS = 2
```

**Frontend**:
```typescript
// customer-frontend/src/config/constants.ts
export const SESSION_TIMEOUT_HOURS = 16;
export const ORDER_TIMEOUT_HOURS = 2;
```

---

## Integration Points

### 1. Customer Frontend ↔ Backend
**Integration Type**: API Integration

**Key Endpoints**:
- Authentication: `/api/auth/table-login`
- Menu: `/api/menus`
- Order: `/api/orders`

**Testing Strategy**: End-to-End Tests (Cypress or Playwright)

---

### 2. Admin Frontend ↔ Backend
**Integration Type**: API + SSE Integration

**Key Endpoints**:
- Authentication: `/api/auth/admin-login`
- Order Management: `/api/admin/orders`
- Table Management: `/api/admin/tables`
- Menu Management: `/api/admin/menus`
- Real-time: `/api/admin/sse/orders`

**Testing Strategy**: End-to-End Tests + SSE Connection Tests

---

## Deployment Dependencies

### Development Order
**Sequential Development** (순차적 개발)

1. **Phase 1: Backend Service**
   - 모든 API 엔드포인트 구현
   - 데이터베이스 스키마 생성
   - 단위 테스트 완료
   - **Output**: 완전히 동작하는 Backend API

2. **Phase 2: Customer Frontend**
   - Backend API 연동
   - 고객 주문 플로우 구현
   - **Depends on**: Backend API 완료
   - **Output**: 고객용 주문 앱

3. **Phase 3: Admin Frontend**
   - Backend API + SSE 연동
   - 관리자 운영 기능 구현
   - **Depends on**: Backend API 완료
   - **Output**: 관리자용 운영 앱

---

## Runtime Dependencies

### Startup Order
1. **Backend Service** (먼저 시작)
   - Database 연결 확인
   - API 서버 시작
   - Port: 8000 (기본값)

2. **Customer Frontend** (Backend 시작 후)
   - Backend API URL 설정
   - Dev Server 시작
   - Port: 5173 (기본값)

3. **Admin Frontend** (Backend 시작 후)
   - Backend API URL 설정
   - SSE 연결 설정
   - Dev Server 시작
   - Port: 5174 (기본값)

---

## Dependency Risks

### Risk 1: Backend API 변경
**Impact**: Frontend 코드 수정 필요  
**Mitigation**: API 버전 관리, 변경 사항 문서화

### Risk 2: SSE 연결 불안정
**Impact**: Admin Frontend 실시간 업데이트 실패  
**Mitigation**: Auto-reconnect 메커니즘, Fallback to polling

### Risk 3: 데이터 모델 불일치
**Impact**: Frontend-Backend 통신 오류  
**Mitigation**: TypeScript 타입 정의, API 응답 검증

---

## Summary

- **Backend Service**: 독립적, 다른 Unit에 API 제공
- **Customer Frontend**: Backend API에 의존
- **Admin Frontend**: Backend API + SSE에 의존
- **Communication**: HTTP REST + SSE
- **Data Sharing**: Duplicate (각 Unit에 복사)
- **Development Order**: Sequential (Backend → Customer → Admin)
- **Integration Testing**: End-to-End Tests

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
