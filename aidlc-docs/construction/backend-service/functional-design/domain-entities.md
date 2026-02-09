# Domain Entities - Backend Service

## Overview

Backend Service의 핵심 도메인 엔티티와 데이터 구조를 정의합니다.

---

## Entity Relationship Diagram (Text Format)

```
Store (매장)
  |
  +-- AdminUser (관리자)
  |
  +-- TableAuth (테이블 인증)
  |     |
  |     +-- TableSession (테이블 세션)
  |           |
  |           +-- Order (주문)
  |                 |
  |                 +-- OrderItem (주문 아이템)
  |
  +-- Category (카테고리)
        |
        +-- Menu (메뉴)
```

---

## 1. Store (매장)

**목적**: 매장 정보 관리

**속성**:
- `id` (Integer, PK): 매장 고유 ID
- `name` (String, 100): 매장 이름
- `created_at` (DateTime): 생성 시각
- `updated_at` (DateTime): 수정 시각

**관계**:
- `admin_users` (1:N): 매장에 속한 관리자들
- `table_auths` (1:N): 매장의 테이블 인증 정보들
- `categories` (1:N): 매장의 메뉴 카테고리들

**비즈니스 규칙**:
- 매장 이름은 필수
- 매장 이름은 중복 불가

---

## 2. AdminUser (관리자)

**목적**: 관리자 계정 관리

**속성**:
- `id` (Integer, PK): 관리자 고유 ID
- `store_id` (Integer, FK): 소속 매장 ID
- `username` (String, 50): 사용자명
- `password_hash` (String, 255): bcrypt 해싱된 비밀번호
- `failed_login_attempts` (Integer, default=0): 로그인 실패 횟수
- `locked_until` (DateTime, nullable): 계정 잠금 해제 시각
- `created_at` (DateTime): 생성 시각
- `updated_at` (DateTime): 수정 시각

**관계**:
- `store` (N:1): 소속 매장

**비즈니스 규칙**:
- username은 매장 내에서 고유해야 함
- 비밀번호는 최소 8자 이상
- 5회 로그인 실패 시 15분 잠금
- 잠금 해제 후 failed_login_attempts 초기화

**인덱스**:
- `(store_id, username)` - 로그인 조회 최적화

---

## 3. TableAuth (테이블 인증)

**목적**: 테이블 태블릿 인증 정보 관리

**속성**:
- `id` (Integer, PK): 테이블 인증 고유 ID
- `store_id` (Integer, FK): 소속 매장 ID
- `table_number` (String, 20): 테이블 번호 (예: "T01", "A-5")
- `password_hash` (String, 255): bcrypt 해싱된 비밀번호
- `failed_login_attempts` (Integer, default=0): 로그인 실패 횟수
- `locked_until` (DateTime, nullable): 계정 잠금 해제 시각
- `created_at` (DateTime): 생성 시각
- `updated_at` (DateTime): 수정 시각

**관계**:
- `store` (N:1): 소속 매장
- `sessions` (1:N): 테이블 세션들

**비즈니스 규칙**:
- table_number는 매장 내에서 고유해야 함
- 비밀번호는 최소 8자 이상
- 5회 로그인 실패 시 15분 잠금

**인덱스**:
- `(store_id, table_number)` - 로그인 조회 최적화

---

## 4. TableSession (테이블 세션)

**목적**: 테이블 사용 세션 관리

**속성**:
- `id` (Integer, PK): 세션 고유 ID
- `table_auth_id` (Integer, FK): 테이블 인증 ID
- `session_token` (String, 255): 세션 토큰 (UUID)
- `created_at` (DateTime): 세션 시작 시각
- `last_order_at` (DateTime, nullable): 마지막 주문 시각
- `expired_at` (DateTime, nullable): 세션 만료 시각
- `closed_at` (DateTime, nullable): 세션 종료 시각 (관리자가 수동 종료)
- `is_active` (Boolean, default=True): 세션 활성 상태

**관계**:
- `table_auth` (N:1): 테이블 인증 정보
- `orders` (1:N): 세션의 주문들

**비즈니스 규칙**:
- 세션 만료 조건:
  - 생성 후 16시간 경과 OR
  - 마지막 주문 후 2시간 경과 (둘 중 먼저 도달)
- 세션 만료 시 is_active = False
- 관리자가 "매장 이용 완료" 처리 시 closed_at 설정 및 is_active = False
- 활성 세션은 테이블당 1개만 존재

**인덱스**:
- `session_token` - 세션 조회 최적화
- `(table_auth_id, is_active)` - 활성 세션 조회 최적화

---

## 5. Category (카테고리)

**목적**: 메뉴 카테고리 관리

**속성**:
- `id` (Integer, PK): 카테고리 고유 ID
- `store_id` (Integer, FK): 소속 매장 ID
- `name` (String, 50): 카테고리 이름 (예: "메인", "사이드", "음료")
- `display_order` (Integer, default=0): 표시 순서
- `created_at` (DateTime): 생성 시각
- `updated_at` (DateTime): 수정 시각

**관계**:
- `store` (N:1): 소속 매장
- `menus` (1:N): 카테고리의 메뉴들

**비즈니스 규칙**:
- 카테고리 이름은 매장 내에서 고유해야 함
- display_order로 정렬하여 표시

**인덱스**:
- `(store_id, display_order)` - 카테고리 목록 조회 최적화

---

## 6. Menu (메뉴)

**목적**: 메뉴 정보 관리

**속성**:
- `id` (Integer, PK): 메뉴 고유 ID
- `store_id` (Integer, FK): 소속 매장 ID
- `category_id` (Integer, FK): 카테고리 ID
- `name` (String, 100): 메뉴 이름
- `description` (Text, nullable): 메뉴 설명
- `price` (Integer): 가격 (원 단위)
- `image_url` (String, 500, nullable): 이미지 URL
- `display_order` (Integer, default=0): 카테고리 내 표시 순서
- `is_available` (Boolean, default=True): 판매 가능 여부
- `created_at` (DateTime): 생성 시각
- `updated_at` (DateTime): 수정 시각

**관계**:
- `store` (N:1): 소속 매장
- `category` (N:1): 소속 카테고리
- `order_items` (1:N): 주문 아이템들

**비즈니스 규칙**:
- 메뉴 이름은 필수
- 가격은 양수여야 함 (> 0)
- is_available = False인 메뉴는 고객에게 표시 안 함

**인덱스**:
- `(category_id, display_order)` - 카테고리별 메뉴 조회 최적화
- `(store_id, is_available)` - 판매 가능 메뉴 조회 최적화

---

## 7. Order (주문)

**목적**: 주문 정보 관리

**속성**:
- `id` (Integer, PK): 주문 고유 ID
- `store_id` (Integer, FK): 소속 매장 ID
- `table_session_id` (Integer, FK): 테이블 세션 ID
- `order_number` (String, 20): 주문 번호 (예: "ORD-20260209-0001")
- `total_amount` (Integer): 총 주문 금액
- `status` (Enum): 주문 상태 ("pending", "preparing", "completed")
- `created_at` (DateTime): 주문 생성 시각
- `updated_at` (DateTime): 주문 수정 시각

**관계**:
- `store` (N:1): 소속 매장
- `table_session` (N:1): 테이블 세션
- `order_items` (1:N): 주문 아이템들

**비즈니스 규칙**:
- order_number는 전체 시스템에서 고유해야 함
- 상태 전이: pending → preparing → completed (순서 준수)
- total_amount는 order_items의 합계와 일치해야 함
- 주문 생성 시 table_session의 last_order_at 업데이트

**인덱스**:
- `order_number` - 주문 번호 조회 최적화
- `(table_session_id, created_at)` - 세션별 주문 조회 최적화
- `(store_id, status, created_at)` - 매장별 상태별 주문 조회 최적화

---

## 8. OrderItem (주문 아이템)

**목적**: 주문의 개별 메뉴 아이템 관리 (스냅샷 포함)

**속성**:
- `id` (Integer, PK): 주문 아이템 고유 ID
- `order_id` (Integer, FK): 주문 ID
- `menu_id` (Integer, FK): 메뉴 ID
- `menu_name` (String, 100): 주문 시점 메뉴 이름 (스냅샷)
- `menu_price` (Integer): 주문 시점 메뉴 가격 (스냅샷)
- `quantity` (Integer): 수량
- `subtotal` (Integer): 소계 (menu_price * quantity)
- `created_at` (DateTime): 생성 시각

**관계**:
- `order` (N:1): 주문
- `menu` (N:1): 메뉴 (참조용)

**비즈니스 규칙**:
- quantity는 양수여야 함 (> 0)
- subtotal = menu_price * quantity
- menu_name과 menu_price는 주문 시점의 값을 스냅샷으로 저장
- 메뉴 정보 변경 시에도 주문 내역은 변경되지 않음

**인덱스**:
- `order_id` - 주문별 아이템 조회 최적화

---

## Entity Summary

| Entity | Purpose | Key Relationships |
|--------|---------|-------------------|
| Store | 매장 정보 | AdminUser, TableAuth, Category |
| AdminUser | 관리자 계정 | Store |
| TableAuth | 테이블 인증 | Store, TableSession |
| TableSession | 테이블 세션 | TableAuth, Order |
| Category | 메뉴 카테고리 | Store, Menu |
| Menu | 메뉴 정보 | Store, Category, OrderItem |
| Order | 주문 | Store, TableSession, OrderItem |
| OrderItem | 주문 아이템 (스냅샷) | Order, Menu |

---

## Data Integrity Rules

### Referential Integrity
- 모든 FK는 NOT NULL (참조 무결성 보장)
- CASCADE DELETE:
  - Store 삭제 시 → AdminUser, TableAuth, Category, Menu, Order 삭제
  - TableAuth 삭제 시 → TableSession 삭제
  - TableSession 삭제 시 → Order 삭제
  - Order 삭제 시 → OrderItem 삭제
  - Category 삭제 시 → Menu의 category_id를 NULL로 설정 (또는 삭제 방지)

### Unique Constraints
- `(store_id, username)` - AdminUser
- `(store_id, table_number)` - TableAuth
- `(store_id, name)` - Category
- `order_number` - Order (전역 고유)

### Check Constraints
- `price > 0` - Menu
- `quantity > 0` - OrderItem
- `total_amount >= 0` - Order
- `failed_login_attempts >= 0` - AdminUser, TableAuth

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
