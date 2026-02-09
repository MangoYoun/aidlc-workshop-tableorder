# Business Rules - Backend Service

## Overview

Backend Service의 비즈니스 규칙, 검증 로직, 제약사항을 정의합니다.

---

## 1. 인증 및 보안 규칙 (Authentication & Security Rules)

### BR-AUTH-001: 비밀번호 복잡도
**규칙**: 모든 비밀번호는 최소 8자 이상이어야 한다.

**적용 대상**:
- 관리자 비밀번호
- 테이블 비밀번호

**검증 시점**: 계정 생성, 비밀번호 변경

**에러 메시지**: "비밀번호는 최소 8자 이상이어야 합니다"

---

### BR-AUTH-002: 로그인 시도 제한
**규칙**: 5회 연속 로그인 실패 시 계정을 15분간 잠근다.

**적용 대상**:
- 관리자 로그인
- 테이블 로그인

**검증 시점**: 로그인 시도

**동작**:
- 로그인 실패 시 `failed_login_attempts` 증가
- `failed_login_attempts >= 5`이면 `locked_until = 현재 시각 + 15분`
- 로그인 성공 시 `failed_login_attempts = 0`, `locked_until = NULL`

**에러 메시지**: "로그인 시도 횟수 초과. {남은 시간}분 후 다시 시도해주세요"

---

### BR-AUTH-003: JWT 토큰 만료
**규칙**: JWT 토큰은 발급 후 16시간 동안 유효하다.

**적용 대상**:
- 관리자 JWT
- 테이블 JWT

**검증 시점**: 모든 API 요청 (Middleware)

**에러 메시지**: "토큰이 만료되었습니다. 다시 로그인해주세요"

---

### BR-AUTH-004: 비밀번호 해싱
**규칙**: 모든 비밀번호는 bcrypt로 해싱하여 저장한다.

**적용 대상**:
- 관리자 비밀번호
- 테이블 비밀번호

**검증 시점**: 계정 생성, 비밀번호 변경

**구현**: Passlib 라이브러리 사용

---

### BR-AUTH-005: 경로 기반 권한 제어
**규칙**: `/api/admin/*` 경로는 관리자만 접근 가능하다.

**적용 대상**:
- 모든 관리자 전용 API

**검증 시점**: API 요청 (Middleware)

**동작**:
- JWT의 `user_type`이 "admin"이 아니면 → 403 Forbidden

**에러 메시지**: "관리자 권한이 필요합니다"

---

## 2. 세션 관리 규칙 (Session Management Rules)

### BR-SESSION-001: 테이블 세션 만료 조건
**규칙**: 테이블 세션은 다음 조건 중 하나라도 만족하면 만료된다.
- 조건 1: 세션 생성 후 16시간 경과
- 조건 2: 마지막 주문 후 2시간 경과

**적용 대상**: TableSession

**검증 시점**: 모든 API 요청 (Middleware)

**동작**:
- 만료 조건 만족 시:
  - `is_active = False`
  - `expired_at = 현재 시각`
  - 401 Unauthorized 에러 반환

**에러 메시지**: "세션이 만료되었습니다. 다시 로그인해주세요"

---

### BR-SESSION-002: 테이블당 활성 세션 제한
**규칙**: 테이블당 활성 세션은 1개만 존재할 수 있다.

**적용 대상**: TableSession

**검증 시점**: 테이블 로그인

**동작**:
- 기존 활성 세션이 있으면 → 기존 세션 반환
- 기존 세션이 만료되었으면 → 새 세션 생성

---

### BR-SESSION-003: 세션 종료 시 주문 불가
**규칙**: 세션이 종료된 후에는 주문을 생성할 수 없다.

**적용 대상**: Order 생성

**검증 시점**: 주문 생성 요청

**동작**:
- `is_active = False`인 세션으로 주문 시도 시 → 401 Unauthorized

**에러 메시지**: "세션이 종료되었습니다. 다시 로그인해주세요"

---

### BR-SESSION-004: 주문 생성 시 세션 연장
**규칙**: 주문 생성 시 `last_order_at`을 현재 시각으로 업데이트한다.

**적용 대상**: TableSession

**검증 시점**: 주문 생성

**동작**:
- Order 생성 성공 시 → `last_order_at = 현재 시각`
- 이로 인해 세션 만료 시간이 2시간 연장됨

---

## 3. 메뉴 관리 규칙 (Menu Management Rules)

### BR-MENU-001: 메뉴 가격 양수 제약
**규칙**: 메뉴 가격은 양수(> 0)여야 한다.

**적용 대상**: Menu

**검증 시점**: 메뉴 생성, 메뉴 수정

**에러 메시지**: "메뉴 가격은 0보다 커야 합니다"

---

### BR-MENU-002: 메뉴 이름 필수
**규칙**: 메뉴 이름은 필수 입력 항목이다.

**적용 대상**: Menu

**검증 시점**: 메뉴 생성, 메뉴 수정

**에러 메시지**: "메뉴 이름은 필수입니다"

---

### BR-MENU-003: 판매 불가 메뉴 숨김
**규칙**: `is_available = False`인 메뉴는 고객에게 표시하지 않는다.

**적용 대상**: Menu 조회 (고객용)

**검증 시점**: 메뉴 목록 조회

**동작**:
- 고객용 API: `is_available = True`인 메뉴만 반환
- 관리자용 API: 모든 메뉴 반환

---

### BR-MENU-004: 판매 불가 메뉴 주문 불가
**규칙**: `is_available = False`인 메뉴는 주문할 수 없다.

**적용 대상**: Order 생성

**검증 시점**: 주문 생성

**에러 메시지**: "해당 메뉴는 현재 판매하지 않습니다 (메뉴명: {menu_name})"

---

### BR-MENU-005: 카테고리 이름 고유성
**규칙**: 카테고리 이름은 매장 내에서 고유해야 한다.

**적용 대상**: Category

**검증 시점**: 카테고리 생성

**에러 메시지**: "이미 존재하는 카테고리 이름입니다"

---

## 4. 주문 관리 규칙 (Order Management Rules)

### BR-ORDER-001: 주문 수량 양수 제약
**규칙**: 주문 수량은 양수(> 0)여야 한다.

**적용 대상**: OrderItem

**검증 시점**: 주문 생성

**에러 메시지**: "주문 수량은 0보다 커야 합니다"

---

### BR-ORDER-002: 주문 번호 고유성
**규칙**: 주문 번호는 전체 시스템에서 고유해야 한다.

**적용 대상**: Order

**검증 시점**: 주문 생성

**형식**: "ORD-{YYYYMMDD}-{sequence}"  
**예시**: "ORD-20260209-0001"

**동작**:
- 날짜별로 sequence 증가 (0001, 0002, ...)
- Database UNIQUE 제약으로 중복 방지

---

### BR-ORDER-003: 주문 상태 전이 규칙
**규칙**: 주문 상태는 정해진 순서대로만 변경할 수 있다.

**상태 전이**:
- `pending` → `preparing`: 허용
- `preparing` → `completed`: 허용
- 기타 모든 전이: 불허

**적용 대상**: Order

**검증 시점**: 주문 상태 변경

**에러 메시지**: "잘못된 상태 전이입니다 (현재: {current_status}, 요청: {new_status})"

---

### BR-ORDER-004: 주문 금액 일치
**규칙**: Order의 `total_amount`는 OrderItem의 `subtotal` 합계와 일치해야 한다.

**적용 대상**: Order, OrderItem

**검증 시점**: 주문 생성

**동작**:
- `total_amount = sum(order_items.subtotal)`
- `subtotal = menu_price * quantity`

---

### BR-ORDER-005: 메뉴 정보 스냅샷
**규칙**: 주문 생성 시 메뉴 이름과 가격을 스냅샷으로 저장한다.

**적용 대상**: OrderItem

**검증 시점**: 주문 생성

**동작**:
- `menu_name = menu.name` (주문 시점)
- `menu_price = menu.price` (주문 시점)
- 이후 Menu 테이블의 정보가 변경되어도 OrderItem은 변경되지 않음

**이유**: 주문 내역의 정확성 보장

---

### BR-ORDER-006: 주문 삭제 시 OrderItem 삭제
**규칙**: Order 삭제 시 관련된 모든 OrderItem도 함께 삭제한다.

**적용 대상**: Order, OrderItem

**검증 시점**: 주문 삭제

**동작**: CASCADE DELETE

---

## 5. 데이터 무결성 규칙 (Data Integrity Rules)

### BR-DATA-001: 외래 키 제약
**규칙**: 모든 외래 키는 참조 무결성을 보장해야 한다.

**적용 대상**: 모든 FK 관계

**동작**:
- FK는 NOT NULL (필수 참조)
- 참조하는 레코드가 없으면 → 에러 반환

**에러 메시지**: "참조하는 {entity}가 존재하지 않습니다"

---

### BR-DATA-002: 고유 제약
**규칙**: 고유 제약이 있는 필드는 중복 값을 가질 수 없다.

**적용 대상**:
- `(store_id, username)` - AdminUser
- `(store_id, table_number)` - TableAuth
- `(store_id, name)` - Category
- `order_number` - Order

**에러 메시지**: "{field}가 이미 존재합니다"

---

### BR-DATA-003: 필수 필드 제약
**규칙**: 필수 필드는 NULL 값을 가질 수 없다.

**적용 대상**: 모든 NOT NULL 필드

**에러 메시지**: "{field}는 필수 입력 항목입니다"

---

## 6. 성능 관련 규칙 (Performance Rules)

### BR-PERF-001: API 응답 시간
**규칙**: 모든 API는 500ms 이내에 응답해야 한다.

**적용 대상**: 모든 API 엔드포인트

**검증 시점**: 성능 테스트

**동작**:
- 데이터베이스 쿼리 최적화
- 인덱스 활용
- N+1 쿼리 방지

---

### BR-PERF-002: 실시간 업데이트 지연
**규칙**: SSE를 통한 실시간 업데이트는 2초 이내에 전달되어야 한다.

**적용 대상**: SSE 이벤트

**검증 시점**: 성능 테스트

**동작**:
- 이벤트 발생 즉시 브로드캐스트
- 네트워크 지연 최소화

---

### BR-PERF-003: 데이터베이스 인덱스
**규칙**: 자주 조회되는 필드에는 인덱스를 생성해야 한다.

**적용 대상**:
- `(store_id, username)` - AdminUser
- `(store_id, table_number)` - TableAuth
- `session_token` - TableSession
- `(table_auth_id, is_active)` - TableSession
- `(store_id, display_order)` - Category
- `(category_id, display_order)` - Menu
- `(store_id, is_available)` - Menu
- `order_number` - Order
- `(table_session_id, created_at)` - Order
- `(store_id, status, created_at)` - Order
- `order_id` - OrderItem

---

## 7. 에러 처리 규칙 (Error Handling Rules)

### BR-ERROR-001: 에러 로깅
**규칙**: 모든 에러는 로그 파일에 기록되어야 한다.

**적용 대상**: 모든 예외 상황

**로그 포맷**:
```
[{timestamp}] [{level}] [request_id={request_id}] [user_id={user_id}] {message}
```

**로그 레벨**:
- ERROR: 서버 오류, 예외 발생
- WARNING: 비정상 상황 (로그인 실패 등)
- INFO: 정상 요청 (주문 생성 등)

---

### BR-ERROR-002: 사용자 친화적 에러 메시지
**규칙**: 에러 메시지는 사용자가 이해하기 쉬운 한글로 작성한다.

**적용 대상**: 모든 API 에러 응답

**형식**:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "사용자 친화적 메시지",
    "details": {}
  }
}
```

---

### BR-ERROR-003: 트랜잭션 롤백
**규칙**: 트랜잭션 중 에러 발생 시 명시적으로 롤백하고 에러를 로깅한다.

**적용 대상**: 모든 트랜잭션

**동작**:
1. 에러 발생
2. 트랜잭션 롤백
3. 에러 로깅
4. 에러 응답 반환

---

## 8. 실시간 통신 규칙 (Real-time Communication Rules)

### BR-SSE-001: 매장 단위 브로드캐스트
**규칙**: SSE 이벤트는 매장 단위로 브로드캐스트한다.

**적용 대상**: SSE 이벤트

**동작**:
- 이벤트 발생 시 `store_id`로 필터링
- 해당 매장의 모든 관리자 연결에 전송

---

### BR-SSE-002: 클라이언트 재연결
**규칙**: SSE 연결이 끊어지면 클라이언트가 자동으로 재연결한다.

**적용 대상**: SSE 연결

**동작**:
- 서버는 연결 상태를 추적하지 않음
- 클라이언트가 재연결 로직 구현

---

## Business Rules Summary

| 카테고리 | 규칙 수 | 핵심 규칙 |
|----------|---------|-----------|
| 인증 및 보안 | 5 | 비밀번호 8자 이상, 5회 실패 시 15분 잠금 |
| 세션 관리 | 4 | 16시간 OR 마지막 주문 후 2시간 만료 |
| 메뉴 관리 | 5 | 가격 양수, 판매 불가 메뉴 숨김 |
| 주문 관리 | 6 | 상태 전이 순서, 메뉴 정보 스냅샷 |
| 데이터 무결성 | 3 | FK 제약, 고유 제약, 필수 필드 |
| 성능 | 3 | API 500ms 이내, SSE 2초 이내 |
| 에러 처리 | 3 | 에러 로깅, 사용자 친화적 메시지 |
| 실시간 통신 | 2 | 매장 단위 브로드캐스트 |

**Total**: 31개 비즈니스 규칙

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
