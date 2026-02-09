# Application Components

## Component Architecture Overview

테이블오더 서비스는 **Component-based Architecture**를 사용하며, **Layered Architecture** 패턴을 따릅니다.

**아키텍처 계층:**
```
Frontend (Vue.js)
├─ Customer App (고객용)
└─ Admin App (관리자용)

Backend (FastAPI)
├─ Controller Layer (API 엔드포인트)
├─ Service Layer (비즈니스 로직)
└─ Repository Layer (데이터 접근)

Database (PostgreSQL)
└─ Data Models
```

---

## Frontend Components

### 1. Customer App Components (고객용)

#### 1.1 MenuView Component
**목적**: 메뉴 조회 및 탐색 화면

**책임**:
- 카테고리별 메뉴 목록 표시
- 메뉴 상세 정보 표시
- 메뉴 선택 및 장바구니 추가

**인터페이스**:
- Props: None (Pinia store에서 데이터 로드)
- Events: `add-to-cart` (메뉴 추가 시)
- Store: `menuStore`, `cartStore`

**하위 컴포넌트**:
- `CategoryTabs`: 카테고리 탭
- `MenuCard`: 개별 메뉴 카드
- `MenuDetail`: 메뉴 상세 모달

---

#### 1.2 CartView Component
**목적**: 장바구니 관리 화면

**책임**:
- 장바구니 아이템 목록 표시
- 수량 조절 (증가/감소)
- 아이템 삭제
- 총 금액 계산 및 표시
- 주문 확정

**인터페이스**:
- Props: None (Pinia store에서 데이터 로드)
- Events: `place-order` (주문 확정 시)
- Store: `cartStore`, `orderStore`

**하위 컴포넌트**:
- `CartItem`: 개별 장바구니 아이템
- `CartSummary`: 총 금액 요약

---

#### 1.3 OrderHistoryView Component
**목적**: 주문 내역 조회 화면

**책임**:
- 현재 테이블 세션의 주문 내역 표시
- 주문 상태 표시
- 주문 상세 정보 표시

**인터페이스**:
- Props: None (Pinia store에서 데이터 로드)
- Events: None
- Store: `orderStore`

**하위 컴포넌트**:
- `OrderCard`: 개별 주문 카드
- `OrderDetail`: 주문 상세 모달

---

#### 1.4 LoginView Component
**목적**: 테이블 자동 로그인 화면

**책임**:
- 초기 설정 시 로그인 정보 입력
- LocalStorage에 로그인 정보 저장
- 자동 로그인 처리

**인터페이스**:
- Props: None
- Events: `login-success` (로그인 성공 시)
- Store: `authStore`

---

### 2. Admin App Components (관리자용)

#### 2.1 AdminLoginView Component
**목적**: 관리자 로그인 화면

**책임**:
- 매장 식별자, 사용자명, 비밀번호 입력
- JWT 토큰 발급 및 저장
- 로그인 성공 시 대시보드로 이동

**인터페이스**:
- Props: None
- Events: `login-success` (로그인 성공 시)
- Store: `adminAuthStore`

---

#### 2.2 OrderDashboardView Component
**목적**: 실시간 주문 모니터링 대시보드

**책임**:
- 테이블별 주문 현황 그리드 표시
- 실시간 주문 업데이트 (SSE)
- 주문 상태 변경
- 신규 주문 강조 표시

**인터페이스**:
- Props: None (Pinia store에서 데이터 로드)
- Events: `update-order-status` (주문 상태 변경 시)
- Store: `adminOrderStore`

**하위 컴포넌트**:
- `TableCard`: 테이블별 주문 카드
- `OrderDetailModal`: 주문 상세 모달
- `SSEConnection`: SSE 연결 관리

---

#### 2.3 TableManagementView Component
**목적**: 테이블 관리 화면

**책임**:
- 테이블 초기 설정
- 주문 삭제
- 테이블 세션 종료 (매장 이용 완료)
- 과거 주문 내역 조회

**인터페이스**:
- Props: None (Pinia store에서 데이터 로드)
- Events: `delete-order`, `complete-session` (주문 삭제, 세션 종료 시)
- Store: `adminTableStore`

**하위 컴포넌트**:
- `TableSetupModal`: 테이블 초기 설정 모달
- `OrderHistoryModal`: 과거 내역 조회 모달

---

#### 2.4 MenuManagementView Component
**목적**: 메뉴 관리 화면

**책임**:
- 메뉴 목록 조회 (카테고리별)
- 메뉴 등록/수정/삭제
- 메뉴 이미지 업로드
- 메뉴 노출 순서 조정

**인터페이스**:
- Props: None (Pinia store에서 데이터 로드)
- Events: `create-menu`, `update-menu`, `delete-menu` (메뉴 CRUD 시)
- Store: `adminMenuStore`

**하위 컴포넌트**:
- `MenuForm`: 메뉴 등록/수정 폼
- `MenuList`: 메뉴 목록
- `ImageUploader`: 이미지 업로드

---

### 3. Shared Components (공통)

#### 3.1 AppHeader Component
**목적**: 앱 헤더 (네비게이션)

**책임**:
- 앱 제목 표시
- 네비게이션 메뉴
- 로그아웃 버튼

**인터페이스**:
- Props: `title` (String), `showLogout` (Boolean)
- Events: `logout` (로그아웃 시)

---

#### 3.2 LoadingSpinner Component
**목적**: 로딩 인디케이터

**책임**:
- 로딩 중 스피너 표시

**인터페이스**:
- Props: `loading` (Boolean)
- Events: None

---

#### 3.3 ErrorMessage Component
**목적**: 에러 메시지 표시

**책임**:
- 에러 메시지 표시
- 에러 타입별 스타일링

**인터페이스**:
- Props: `message` (String), `type` (String: 'error' | 'warning' | 'info')
- Events: `close` (닫기 시)

---

## Backend Components

### 1. Controller Layer (API 엔드포인트)

#### 1.1 AuthController
**목적**: 인증 관련 API 엔드포인트

**책임**:
- 테이블 로그인 처리
- 관리자 로그인 처리
- JWT 토큰 발급
- 토큰 검증

**인터페이스**:
- Endpoints:
  - `POST /api/auth/table/login` - 테이블 로그인
  - `POST /api/auth/admin/login` - 관리자 로그인
  - `POST /api/auth/refresh` - 토큰 갱신

**의존성**: `AuthService`

---

#### 1.2 MenuController
**목적**: 메뉴 관련 API 엔드포인트

**책임**:
- 메뉴 조회 (고객용)
- 메뉴 CRUD (관리자용)

**인터페이스**:
- Endpoints:
  - `GET /api/menus` - 메뉴 목록 조회
  - `GET /api/menus/{menu_id}` - 메뉴 상세 조회
  - `POST /api/admin/menus` - 메뉴 등록
  - `PUT /api/admin/menus/{menu_id}` - 메뉴 수정
  - `DELETE /api/admin/menus/{menu_id}` - 메뉴 삭제

**의존성**: `MenuService`

---

#### 1.3 OrderController
**목적**: 주문 관련 API 엔드포인트

**책임**:
- 주문 생성 (고객용)
- 주문 조회 (고객용, 관리자용)
- 주문 상태 변경 (관리자용)
- 주문 삭제 (관리자용)

**인터페이스**:
- Endpoints:
  - `POST /api/orders` - 주문 생성
  - `GET /api/orders` - 주문 내역 조회 (현재 세션)
  - `GET /api/admin/orders` - 모든 주문 조회
  - `PUT /api/admin/orders/{order_id}/status` - 주문 상태 변경
  - `DELETE /api/admin/orders/{order_id}` - 주문 삭제

**의존성**: `OrderService`

---

#### 1.4 TableController
**목적**: 테이블 관리 API 엔드포인트

**책임**:
- 테이블 초기 설정
- 테이블 세션 종료
- 과거 주문 내역 조회

**인터페이스**:
- Endpoints:
  - `POST /api/admin/tables/setup` - 테이블 초기 설정
  - `POST /api/admin/tables/{table_id}/complete` - 테이블 세션 종료
  - `GET /api/admin/tables/{table_id}/history` - 과거 주문 내역

**의존성**: `TableService`

---

#### 1.5 SSEController
**목적**: 실시간 통신 API 엔드포인트

**책임**:
- SSE 연결 관리
- 실시간 주문 업데이트 전송

**인터페이스**:
- Endpoints:
  - `GET /api/admin/orders/stream` - SSE 연결 (실시간 주문 업데이트)

**의존성**: `OrderService`, `SSEService`

---

### 2. Service Layer (비즈니스 로직)

#### 2.1 AuthService
**목적**: 인증 및 권한 관리 비즈니스 로직

**책임**:
- 로그인 검증
- JWT 토큰 생성 및 검증
- 비밀번호 해싱 및 검증
- 세션 관리

**인터페이스**:
- Methods: (상세 메서드는 component-methods.md 참조)
- Dependencies: `UserRepository`, `TableRepository`

---

#### 2.2 MenuService
**목적**: 메뉴 관리 비즈니스 로직

**책임**:
- 메뉴 CRUD 로직
- 메뉴 검증
- 이미지 업로드 처리
- 메뉴 순서 조정

**인터페이스**:
- Methods: (상세 메서드는 component-methods.md 참조)
- Dependencies: `MenuRepository`

---

#### 2.3 OrderService
**목적**: 주문 관리 비즈니스 로직

**책임**:
- 주문 생성 로직
- 주문 검증
- 주문 상태 관리
- 주문 금액 계산
- 실시간 주문 알림

**인터페이스**:
- Methods: (상세 메서드는 component-methods.md 참조)
- Dependencies: `OrderRepository`, `MenuRepository`, `SSEService`

---

#### 2.4 TableService
**목적**: 테이블 관리 비즈니스 로직

**책임**:
- 테이블 세션 관리
- 테이블 초기 설정
- 세션 만료 처리
- 과거 주문 이력 관리

**인터페이스**:
- Methods: (상세 메서드는 component-methods.md 참조)
- Dependencies: `TableRepository`, `OrderRepository`

---

#### 2.5 SSEService
**목적**: 실시간 통신 관리

**책임**:
- SSE 연결 관리
- 클라이언트 연결 추적
- 이벤트 브로드캐스트

**인터페이스**:
- Methods: (상세 메서드는 component-methods.md 참조)
- Dependencies: None

---

### 3. Repository Layer (데이터 접근)

#### 3.1 UserRepository
**목적**: 사용자 (관리자) 데이터 접근

**책임**:
- 사용자 조회
- 사용자 생성/수정

**인터페이스**:
- Methods: (상세 메서드는 component-methods.md 참조)
- ORM: SQLAlchemy

---

#### 3.2 TableRepository
**목적**: 테이블 데이터 접근

**책임**:
- 테이블 조회
- 테이블 생성/수정
- 테이블 세션 관리

**인터페이스**:
- Methods: (상세 메서드는 component-methods.md 참조)
- ORM: SQLAlchemy

---

#### 3.3 MenuRepository
**목적**: 메뉴 데이터 접근

**책임**:
- 메뉴 CRUD
- 카테고리별 메뉴 조회

**인터페이스**:
- Methods: (상세 메서드는 component-methods.md 참조)
- ORM: SQLAlchemy

---

#### 3.4 OrderRepository
**목적**: 주문 데이터 접근

**책임**:
- 주문 CRUD
- 주문 내역 조회
- 주문 상태 업데이트

**인터페이스**:
- Methods: (상세 메서드는 component-methods.md 참조)
- ORM: SQLAlchemy

---

## Component Summary

### Frontend Components
- **Customer App**: 4개 View 컴포넌트 + 하위 컴포넌트
- **Admin App**: 4개 View 컴포넌트 + 하위 컴포넌트
- **Shared**: 3개 공통 컴포넌트

### Backend Components
- **Controller Layer**: 5개 Controller
- **Service Layer**: 5개 Service
- **Repository Layer**: 4개 Repository

**총 컴포넌트 수**: 25개 이상 (하위 컴포넌트 포함)

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
