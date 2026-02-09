# Business Logic Model - Backend Service

## Overview

Backend Service의 핵심 비즈니스 로직, 워크플로우, 데이터 변환 프로세스를 정의합니다.

---

## 1. 인증 및 세션 관리 (Authentication & Session Management)

### 1.1 테이블 자동 로그인 워크플로우

**Input**:
- `store_id` (Integer): 매장 ID
- `table_number` (String): 테이블 번호
- `password` (String): 테이블 비밀번호

**Process**:
1. TableAuth 조회 (store_id, table_number)
2. 계정 잠금 상태 확인
   - locked_until이 현재 시각보다 미래면 → 에러 반환 (계정 잠금)
3. 비밀번호 검증 (bcrypt.verify)
   - 실패 시:
     - failed_login_attempts += 1
     - failed_login_attempts >= 5이면 locked_until = 현재 + 15분
     - 에러 반환 (인증 실패)
   - 성공 시:
     - failed_login_attempts = 0
     - locked_until = NULL
4. 활성 TableSession 조회
   - 존재하고 유효하면 → 기존 세션 반환
   - 없거나 만료되었으면 → 새 세션 생성
5. JWT 토큰 생성
   - Payload: `{user_type: "table", table_auth_id, session_id, store_id}`
   - Expiration: 16시간

**Output**:
- `access_token` (String): JWT 토큰
- `session_id` (Integer): 세션 ID
- `table_number` (String): 테이블 번호

**Business Rules**:
- 5회 로그인 실패 시 15분 잠금
- 테이블당 활성 세션은 1개만 존재
- 세션 만료 조건: 16시간 OR 마지막 주문 후 2시간

---

### 1.2 관리자 로그인 워크플로우

**Input**:
- `store_id` (Integer): 매장 ID
- `username` (String): 사용자명
- `password` (String): 비밀번호

**Process**:
1. AdminUser 조회 (store_id, username)
2. 계정 잠금 상태 확인
   - locked_until이 현재 시각보다 미래면 → 에러 반환 (계정 잠금)
3. 비밀번호 검증 (bcrypt.verify)
   - 실패 시:
     - failed_login_attempts += 1
     - failed_login_attempts >= 5이면 locked_until = 현재 + 15분
     - 에러 반환 (인증 실패)
   - 성공 시:
     - failed_login_attempts = 0
     - locked_until = NULL
4. JWT 토큰 생성
   - Payload: `{user_type: "admin", admin_user_id, store_id}`
   - Expiration: 16시간

**Output**:
- `access_token` (String): JWT 토큰
- `admin_user_id` (Integer): 관리자 ID
- `username` (String): 사용자명

**Business Rules**:
- 5회 로그인 실패 시 15분 잠금
- 관리자는 세션 개념 없음 (JWT만 사용)

---

### 1.3 세션 유효성 검증 (Middleware)

**Input**:
- `session_id` (Integer): 세션 ID (JWT에서 추출)

**Process**:
1. TableSession 조회
2. is_active = False이면 → 에러 반환 (세션 종료됨)
3. 세션 만료 조건 체크:
   - 조건 1: created_at + 16시간 < 현재 시각
   - 조건 2: last_order_at + 2시간 < 현재 시각 (last_order_at이 NULL이 아닌 경우)
   - 둘 중 하나라도 만족하면:
     - is_active = False
     - expired_at = 현재 시각
     - 에러 반환 (세션 만료)
4. 유효한 세션이면 → 요청 계속 진행

**Output**:
- 세션 유효: 요청 진행
- 세션 무효: 401 Unauthorized 에러

---

## 2. 메뉴 관리 (Menu Management)

### 2.1 메뉴 조회 워크플로우

**Input**:
- `store_id` (Integer): 매장 ID
- `category_id` (Integer, optional): 카테고리 ID

**Process**:
1. Category 목록 조회 (store_id, display_order 정렬)
2. 각 Category별로 Menu 조회
   - 조건: is_available = True
   - 정렬: display_order
3. 메뉴 데이터 변환
   - image_url이 NULL이면 기본 이미지 URL 사용

**Output**:
```json
{
  "categories": [
    {
      "id": 1,
      "name": "메인",
      "menus": [
        {
          "id": 101,
          "name": "김치찌개",
          "description": "얼큰한 김치찌개",
          "price": 8000,
          "image_url": "https://..."
        }
      ]
    }
  ]
}
```

**Business Rules**:
- is_available = False인 메뉴는 고객에게 표시 안 함
- 카테고리와 메뉴는 display_order로 정렬

---

### 2.2 메뉴 등록/수정 워크플로우 (관리자)

**Input**:
- `name` (String): 메뉴 이름
- `description` (String, optional): 메뉴 설명
- `price` (Integer): 가격
- `category_id` (Integer): 카테고리 ID
- `image_file` (File, optional): 이미지 파일

**Process**:
1. 입력 검증
   - name: 필수, 최대 100자
   - price: 양수 (> 0)
   - category_id: 존재하는 카테고리인지 확인
2. 이미지 업로드 (있는 경우)
   - 파일 저장 (로컬 또는 S3)
   - image_url 생성
3. Menu 생성/수정
   - display_order: 카테고리 내 마지막 순서 + 1
   - is_available: True (기본값)

**Output**:
- `menu_id` (Integer): 메뉴 ID
- `message` (String): 성공 메시지

**Business Rules**:
- 가격은 양수여야 함
- 이미지는 선택사항

---

## 3. 주문 관리 (Order Management)

### 3.1 주문 생성 워크플로우

**Input**:
- `session_id` (Integer): 테이블 세션 ID
- `items` (Array): 주문 아이템 목록
  - `menu_id` (Integer): 메뉴 ID
  - `quantity` (Integer): 수량

**Process**:
1. 세션 유효성 검증 (Middleware에서 수행)
2. 트랜잭션 시작
3. 각 아이템에 대해:
   - Menu 조회 (menu_id)
   - is_available = False이면 → 에러 반환 (판매 불가 메뉴)
   - OrderItem 생성:
     - menu_name = menu.name (스냅샷)
     - menu_price = menu.price (스냅샷)
     - subtotal = menu_price * quantity
4. Order 생성:
   - order_number = "ORD-{YYYYMMDD}-{sequence}" (예: "ORD-20260209-0001")
   - total_amount = sum(subtotal)
   - status = "pending"
5. TableSession 업데이트:
   - last_order_at = 현재 시각
6. SSE 이벤트 발송 (관리자에게)
   - Event: "order-created"
   - Data: Order 정보
7. 트랜잭션 커밋

**Output**:
```json
{
  "order_id": 123,
  "order_number": "ORD-20260209-0001",
  "total_amount": 16000,
  "status": "pending",
  "created_at": "2026-02-09T14:30:00Z"
}
```

**Business Rules**:
- 주문 생성 시 메뉴 정보를 스냅샷으로 저장
- 주문 생성 시 last_order_at 업데이트 (세션 만료 시간 연장)
- 판매 불가 메뉴는 주문 불가
- 트랜잭션으로 원자성 보장

---

### 3.2 주문 상태 변경 워크플로우 (관리자)

**Input**:
- `order_id` (Integer): 주문 ID
- `new_status` (String): 새 상태 ("preparing", "completed")

**Process**:
1. Order 조회
2. 상태 전이 검증:
   - pending → preparing: 허용
   - preparing → completed: 허용
   - 기타: 에러 반환 (잘못된 상태 전이)
3. Order 업데이트:
   - status = new_status
   - updated_at = 현재 시각
4. SSE 이벤트 발송 (관리자에게)
   - Event: "order-updated"
   - Data: Order 정보

**Output**:
- `order_id` (Integer): 주문 ID
- `status` (String): 새 상태
- `message` (String): 성공 메시지

**Business Rules**:
- 상태 전이 순서: pending → preparing → completed
- 역방향 전이 불가 (completed → preparing 불가)
- 잘못된 전이 시도 시 400 Bad Request 에러

---

### 3.3 주문 내역 조회 워크플로우

**Input**:
- `session_id` (Integer): 테이블 세션 ID (고객용)
- `store_id` (Integer): 매장 ID (관리자용)

**Process**:
1. 고객용 (테이블):
   - Order 조회 (session_id, created_at 역순)
   - OrderItem 조회 (각 Order별)
2. 관리자용:
   - Order 조회 (store_id, status별 필터링 가능, created_at 역순)
   - OrderItem 조회 (각 Order별)
3. 데이터 변환:
   - Order + OrderItem 조인
   - 총 주문액 계산

**Output**:
```json
{
  "orders": [
    {
      "order_id": 123,
      "order_number": "ORD-20260209-0001",
      "total_amount": 16000,
      "status": "preparing",
      "created_at": "2026-02-09T14:30:00Z",
      "items": [
        {
          "menu_name": "김치찌개",
          "menu_price": 8000,
          "quantity": 2,
          "subtotal": 16000
        }
      ]
    }
  ]
}
```

**Business Rules**:
- 고객은 현재 세션의 주문만 조회 가능
- 관리자는 매장의 모든 주문 조회 가능
- 세션 종료된 주문은 고객에게 표시 안 함

---

## 4. 테이블 관리 (Table Management)

### 4.1 테이블 세션 종료 워크플로우 (관리자)

**Input**:
- `session_id` (Integer): 세션 ID

**Process**:
1. TableSession 조회
2. 세션 종료 처리:
   - is_active = False
   - closed_at = 현재 시각
3. 해당 세션의 모든 Order를 OrderHistory로 이동 (선택사항)
   - 또는 Order 테이블에 그대로 유지 (is_active = False로 필터링)

**Output**:
- `session_id` (Integer): 세션 ID
- `message` (String): "매장 이용 완료 처리됨"

**Business Rules**:
- 세션 종료 시 고객은 더 이상 주문 불가
- 세션 종료 시 장바구니 초기화 (Frontend에서 처리)
- 과거 주문 내역은 보존

---

### 4.2 주문 삭제 워크플로우 (관리자)

**Input**:
- `order_id` (Integer): 주문 ID

**Process**:
1. Order 조회
2. 트랜잭션 시작
3. OrderItem 삭제 (order_id)
4. Order 삭제
5. 테이블 총 주문액 재계산 (해당 세션의 남은 주문들)
6. 트랜잭션 커밋
7. SSE 이벤트 발송 (관리자에게)
   - Event: "order-deleted"
   - Data: order_id

**Output**:
- `message` (String): "주문이 삭제되었습니다"

**Business Rules**:
- 주문 삭제 시 OrderItem도 함께 삭제 (CASCADE)
- 삭제 후 총 주문액 재계산

---

## 5. 실시간 통신 (Real-time Communication)

### 5.1 SSE 이벤트 브로드캐스트

**Event Types**:
- `order-created`: 신규 주문 생성
- `order-updated`: 주문 상태 변경
- `order-deleted`: 주문 삭제

**Process**:
1. 이벤트 발생 (주문 생성/수정/삭제)
2. 매장 ID로 필터링
3. 해당 매장의 모든 관리자 SSE 연결에 브로드캐스트
4. 이벤트 데이터:
   ```json
   {
     "event": "order-created",
     "data": {
       "order_id": 123,
       "order_number": "ORD-20260209-0001",
       "table_number": "T01",
       "total_amount": 16000,
       "status": "pending",
       "created_at": "2026-02-09T14:30:00Z"
     }
   }
   ```

**Business Rules**:
- 매장 단위로 브로드캐스트
- 연결 끊김 시 클라이언트 자동 재연결
- 2초 이내 전달 (성능 요구사항)

---

## 6. 데이터 변환 및 검증

### 6.1 입력 검증 규칙

**공통 규칙**:
- 필수 필드 누락 시 → 400 Bad Request
- 타입 불일치 시 → 400 Bad Request
- 범위 초과 시 → 400 Bad Request

**필드별 규칙**:
- `price`: 양수 (> 0)
- `quantity`: 양수 (> 0)
- `password`: 최소 8자 이상
- `email`: 이메일 형식 (선택사항)
- `table_number`: 최대 20자
- `menu_name`: 최대 100자

### 6.2 출력 데이터 변환

**DateTime 형식**:
- ISO 8601 형식: "2026-02-09T14:30:00Z"

**금액 형식**:
- Integer (원 단위)
- 예: 8000 (8,000원)

**이미지 URL**:
- 절대 경로 반환
- NULL인 경우 기본 이미지 URL

---

## 7. 에러 처리 전략

### 7.1 에러 분류

**Client Errors (4xx)**:
- 400 Bad Request: 입력 검증 실패
- 401 Unauthorized: 인증 실패, 세션 만료
- 403 Forbidden: 권한 없음
- 404 Not Found: 리소스 없음

**Server Errors (5xx)**:
- 500 Internal Server Error: 서버 내부 오류
- 503 Service Unavailable: 서비스 일시 중단

### 7.2 에러 응답 형식

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "가격은 양수여야 합니다",
    "details": {
      "field": "price",
      "value": -1000
    }
  }
}
```

### 7.3 에러 로깅

**로그 레벨**:
- ERROR: 서버 오류, 예외 발생
- WARNING: 비정상 상황 (로그인 실패 등)
- INFO: 정상 요청 (주문 생성 등)
- DEBUG: 디버깅 정보

**로그 포맷**:
```
[2026-02-09 14:30:00] [ERROR] [request_id=abc123] [user_id=456] Order creation failed: Menu not available (menu_id=789)
```

---

## Business Logic Summary

| 기능 | 핵심 로직 | 트랜잭션 필요 |
|------|-----------|---------------|
| 테이블 로그인 | 비밀번호 검증 + 세션 생성 | No |
| 관리자 로그인 | 비밀번호 검증 + JWT 발급 | No |
| 세션 유효성 검증 | 만료 조건 체크 | No |
| 메뉴 조회 | 카테고리별 필터링 + 정렬 | No |
| 메뉴 등록/수정 | 입력 검증 + 이미지 업로드 | No |
| 주문 생성 | 스냅샷 저장 + SSE 발송 | Yes |
| 주문 상태 변경 | 상태 전이 검증 + SSE 발송 | No |
| 주문 내역 조회 | 세션/매장별 필터링 | No |
| 세션 종료 | 세션 비활성화 | No |
| 주문 삭제 | OrderItem 삭제 + SSE 발송 | Yes |

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
