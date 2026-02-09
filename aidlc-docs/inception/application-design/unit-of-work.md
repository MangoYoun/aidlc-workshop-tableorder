# Units of Work

## Unit 개요

테이블오더 서비스는 **3개의 Units of Work**로 구성됩니다:

1. **Unit 1: Backend Service**
2. **Unit 2: Customer Frontend**
3. **Unit 3: Admin Frontend**

**배포 모델**: Monorepo (단일 저장소)

---

## Unit 1: Backend Service

### 책임
- RESTful API 제공
- 비즈니스 로직 처리
- 데이터베이스 관리
- 인증 및 권한 관리
- 실시간 통신 (SSE)

### 기술 스택
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **Real-time**: Server-Sent Events (SSE)

### 아키텍처
**Modular Monolith** - 하나의 서비스, 모듈로 논리적 분리

**모듈 구조:**
```
backend/
├── app/
│   ├── main.py (FastAPI app)
│   ├── config.py (설정)
│   ├── database.py (DB 연결)
│   ├── middleware/ (인증 middleware)
│   ├── modules/
│   │   ├── auth/ (인증 모듈)
│   │   │   ├── controller.py
│   │   │   ├── service.py
│   │   │   └── repository.py
│   │   ├── menu/ (메뉴 모듈)
│   │   ├── order/ (주문 모듈)
│   │   ├── table/ (테이블 모듈)
│   │   └── sse/ (실시간 통신 모듈)
│   ├── models/ (데이터 모델)
│   └── schemas/ (Pydantic 스키마)
├── tests/
├── requirements.txt
└── .env
```

### 컴포넌트
- **Controllers**: 5개 (Auth, Menu, Order, Table, SSE)
- **Services**: 5개 (Auth, Menu, Order, Table, SSE)
- **Repositories**: 4개 (User, Table, Menu, Order)

### 담당 Stories
- Epic 3: 비기능 요구사항 (3 stories)
  - Story 3.1: 성능 요구사항
  - Story 3.2: 보안 요구사항
  - Story 3.3: 가용성 요구사항

### 복잡도
- **Story Count**: 3 stories
- **Component Count**: 14 components
- **예상 개발 시간**: Medium

### 의존성
- **Depends on**: None
- **Used by**: Customer Frontend, Admin Frontend

---

## Unit 2: Customer Frontend

### 책임
- 고객용 주문 인터페이스
- 메뉴 조회 및 선택
- 장바구니 관리
- 주문 생성 및 내역 조회
- 테이블 자동 로그인

### 기술 스택
- **Framework**: Vue.js 3
- **State Management**: Pinia
- **HTTP Client**: Axios
- **Routing**: Vue Router
- **UI**: Tailwind CSS (또는 선택한 UI 프레임워크)

### 아키텍처
**Component-based Architecture**

**디렉토리 구조:**
```
customer-frontend/
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── router/ (라우팅)
│   ├── stores/ (Pinia stores)
│   │   ├── auth.js
│   │   ├── menu.js
│   │   ├── cart.js
│   │   └── order.js
│   ├── views/ (페이지 컴포넌트)
│   │   ├── LoginView.vue
│   │   ├── MenuView.vue
│   │   ├── CartView.vue
│   │   └── OrderHistoryView.vue
│   ├── components/ (재사용 컴포넌트)
│   │   ├── CategoryTabs.vue
│   │   ├── MenuCard.vue
│   │   ├── CartItem.vue
│   │   └── shared/ (공통 컴포넌트)
│   ├── services/ (API 호출)
│   │   └── api.js
│   └── types/ (TypeScript 타입 - 선택사항)
├── public/
├── package.json
└── vite.config.js
```

### 컴포넌트
- **Views**: 4개 (Login, Menu, Cart, OrderHistory)
- **Components**: 10+ 개 (하위 컴포넌트 포함)
- **Stores**: 4개 (auth, menu, cart, order)

### 담당 Stories
- Epic 1: 고객 주문 여정 (5 stories)
  - Story 1.1: 테이블 자동 로그인
  - Story 1.2: 메뉴 조회 및 탐색
  - Story 1.3: 장바구니 관리
  - Story 1.4: 주문 생성
  - Story 1.5: 주문 내역 조회

### 복잡도
- **Story Count**: 5 stories
- **Component Count**: 14+ components
- **예상 개발 시간**: Medium-High

### 의존성
- **Depends on**: Backend Service (API)
- **Used by**: None

---

## Unit 3: Admin Frontend

### 책임
- 관리자용 운영 인터페이스
- 실시간 주문 모니터링
- 테이블 관리
- 메뉴 관리
- 관리자 인증

### 기술 스택
- **Framework**: Vue.js 3
- **State Management**: Pinia
- **HTTP Client**: Axios
- **Routing**: Vue Router
- **Real-time**: EventSource (SSE)
- **UI**: Tailwind CSS (또는 선택한 UI 프레임워크)

### 아키텍처
**Component-based Architecture**

**디렉토리 구조:**
```
admin-frontend/
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── router/ (라우팅)
│   ├── stores/ (Pinia stores)
│   │   ├── adminAuth.js
│   │   ├── adminOrder.js
│   │   ├── adminTable.js
│   │   └── adminMenu.js
│   ├── views/ (페이지 컴포넌트)
│   │   ├── AdminLoginView.vue
│   │   ├── OrderDashboardView.vue
│   │   ├── TableManagementView.vue
│   │   └── MenuManagementView.vue
│   ├── components/ (재사용 컴포넌트)
│   │   ├── TableCard.vue
│   │   ├── OrderDetailModal.vue
│   │   ├── MenuForm.vue
│   │   └── shared/ (공통 컴포넌트)
│   ├── services/ (API 호출, SSE)
│   │   ├── api.js
│   │   └── sse.js
│   └── types/ (TypeScript 타입 - 선택사항)
├── public/
├── package.json
└── vite.config.js
```

### 컴포넌트
- **Views**: 4개 (AdminLogin, OrderDashboard, TableManagement, MenuManagement)
- **Components**: 10+ 개 (하위 컴포넌트 포함)
- **Stores**: 4개 (adminAuth, adminOrder, adminTable, adminMenu)

### 담당 Stories
- Epic 2: 관리자 운영 여정 (4 stories)
  - Story 2.1: 매장 인증
  - Story 2.2: 실시간 주문 모니터링
  - Story 2.3: 테이블 관리
  - Story 2.4: 메뉴 관리

### 복잡도
- **Story Count**: 4 stories
- **Component Count**: 14+ components
- **예상 개발 시간**: Medium-High

### 의존성
- **Depends on**: Backend Service (API, SSE)
- **Used by**: None

---

## Monorepo 구조

```
table-order-service/
├── backend/ (Unit 1)
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   └── .env
├── customer-frontend/ (Unit 2)
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── admin-frontend/ (Unit 3)
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── aidlc-docs/ (문서)
├── README.md
└── .gitignore
```

---

## 개발 순서

**Sequential Development** (순차적 개발)

1. **Phase 1: Backend Service** (Unit 1)
   - 모든 API 엔드포인트 구현
   - 데이터베이스 스키마 생성
   - 인증 및 권한 관리
   - 단위 테스트

2. **Phase 2: Customer Frontend** (Unit 2)
   - Backend API 연동
   - 고객 주문 플로우 구현
   - 장바구니 LocalStorage 관리
   - 통합 테스트

3. **Phase 3: Admin Frontend** (Unit 3)
   - Backend API 연동
   - 실시간 주문 모니터링 (SSE)
   - 테이블 및 메뉴 관리
   - End-to-End 테스트

---

## 공통 코드 관리

**Strategy**: Duplicate (각 Unit에 복사)

**공통 요소:**
- **DTO/Schema**: Backend의 Pydantic 스키마를 Frontend TypeScript 타입으로 복사
- **API 엔드포인트**: Frontend에서 API URL 상수 정의
- **공통 컴포넌트**: Customer와 Admin Frontend에서 필요시 복사

**이유**: 초보자에게 가장 간단하며, 각 Unit이 독립적으로 동작

---

## Unit Summary

| Unit | Type | Stories | Components | Complexity | Dependencies |
|------|------|---------|------------|------------|--------------|
| Backend Service | Backend | 3 | 14 | Medium | None |
| Customer Frontend | Frontend | 5 | 14+ | Medium-High | Backend |
| Admin Frontend | Frontend | 4 | 14+ | Medium-High | Backend |

**Total**: 3 Units, 12 Stories, 42+ Components

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
