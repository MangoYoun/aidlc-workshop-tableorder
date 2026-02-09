# Test Plan for Backend Service

## Unit Overview

**Unit**: Backend Service  
**Stories**: Story 3.1 (성능), Story 3.2 (보안), Story 3.3 (가용성)  
**Requirements**: REQ-PERF-001, REQ-SEC-001~005, REQ-AVAIL-001~003

---

## Test Strategy

**TDD Approach**: RED-GREEN-REFACTOR 사이클  
**Test Framework**: pytest  
**Coverage Target**: 80% 이상

---

## 1. AuthService Tests

### AuthService.login_admin()

**TC-BS-001**: 유효한 관리자 로그인
- Given: 유효한 store_id, username, password
- When: login_admin() 호출
- Then: JWT 토큰 반환
- Story: 3.2 (보안)
- Status: ⬜ Not Started

**TC-BS-002**: 잘못된 비밀번호로 로그인 시도
- Given: 유효한 username, 잘못된 password
- When: login_admin() 호출
- Then: AuthenticationError 발생, failed_login_attempts 증가
- Story: 3.2 (보안)
- Status: ⬜ Not Started

**TC-BS-003**: 5회 로그인 실패 후 계정 잠금
- Given: 4회 실패한 계정
- When: 5번째 실패 시도
- Then: AccountLockedError 발생, locked_until 설정 (15분 후)
- Story: 3.2 (보안)
- Status: ⬜ Not Started

**TC-BS-004**: 잠긴 계정으로 로그인 시도
- Given: 잠긴 계정 (locked_until이 미래)
- When: login_admin() 호출
- Then: AccountLockedError 발생
- Story: 3.2 (보안)
- Status: ⬜ Not Started

### AuthService.login_table()

**TC-BS-005**: 유효한 테이블 로그인
- Given: 유효한 store_id, table_number, password
- When: login_table() 호출
- Then: 세션 토큰 반환, TableSession 생성
- Story: 3.2 (보안)
- Status: ⬜ Not Started

**TC-BS-006**: 테이블 로그인 실패 및 잠금
- Given: 4회 실패한 테이블
- When: 5번째 실패 시도
- Then: AccountLockedError 발생
- Story: 3.2 (보안)
- Status: ⬜ Not Started

### AuthService.verify_jwt_token()

**TC-BS-007**: 유효한 JWT 토큰 검증
- Given: 유효한 JWT 토큰
- When: verify_jwt_token() 호출
- Then: 페이로드 반환 (user_id, user_type, store_id)
- Story: 3.2 (보안)
- Status: ⬜ Not Started

**TC-BS-008**: 만료된 JWT 토큰 검증
- Given: 만료된 JWT 토큰
- When: verify_jwt_token() 호출
- Then: InvalidTokenError 발생
- Story: 3.2 (보안)
- Status: ⬜ Not Started

### AuthService.verify_session_token()

**TC-BS-009**: 유효한 세션 토큰 검증
- Given: 유효한 세션 토큰
- When: verify_session_token() 호출
- Then: TableSession 객체 반환
- Story: 3.2 (보안)
- Status: ⬜ Not Started

**TC-BS-010**: 만료된 세션 토큰 검증
- Given: 만료된 세션 (16시간 경과)
- When: verify_session_token() 호출
- Then: SessionExpiredError 발생
- Story: 3.3 (가용성)
- Status: ⬜ Not Started

---

## 2. MenuService Tests

### MenuService.get_menus_by_store()

**TC-BS-011**: 매장의 메뉴 목록 조회
- Given: 매장 ID
- When: get_menus_by_store() 호출
- Then: 메뉴 목록 반환 (is_available=True만)
- Story: 3.1 (성능)
- Status: ⬜ Not Started

### MenuService.create_menu()

**TC-BS-012**: 유효한 메뉴 생성
- Given: 유효한 메뉴 정보 (name, price > 0)
- When: create_menu() 호출
- Then: Menu 객체 반환
- Story: 3.2 (보안)
- Status: ⬜ Not Started

**TC-BS-013**: 가격이 0 이하인 메뉴 생성 시도
- Given: price <= 0
- When: create_menu() 호출
- Then: ValidationError 발생
- Story: 3.2 (보안)
- Status: ⬜ Not Started

---

## 3. OrderService Tests

### OrderService.create_order()

**TC-BS-014**: 유효한 주문 생성
- Given: 유효한 세션 토큰, 주문 아이템 목록
- When: create_order() 호출
- Then: Order 객체 반환, order_number 생성, total_amount 계산
- Story: 3.1 (성능)
- Status: ⬜ Not Started

**TC-BS-015**: 만료된 세션으로 주문 생성 시도
- Given: 만료된 세션 토큰
- When: create_order() 호출
- Then: SessionExpiredError 발생
- Story: 3.3 (가용성)
- Status: ⬜ Not Started

**TC-BS-016**: 수량이 0 이하인 주문 생성 시도
- Given: quantity <= 0
- When: create_order() 호출
- Then: ValidationError 발생
- Story: 3.2 (보안)
- Status: ⬜ Not Started

**TC-BS-017**: 주문 생성 시 last_order_at 업데이트
- Given: 유효한 주문 생성
- When: create_order() 호출
- Then: TableSession.last_order_at 업데이트
- Story: 3.3 (가용성)
- Status: ⬜ Not Started

### OrderService.update_order_status()

**TC-BS-018**: 유효한 상태 전이 (pending → preparing)
- Given: status="pending"인 주문
- When: update_order_status(order_id, "preparing") 호출
- Then: 상태 변경 성공
- Story: 3.1 (성능)
- Status: ⬜ Not Started

**TC-BS-019**: 잘못된 상태 전이 (completed → pending)
- Given: status="completed"인 주문
- When: update_order_status(order_id, "pending") 호출
- Then: InvalidStatusTransitionError 발생
- Story: 3.2 (보안)
- Status: ⬜ Not Started

---

## 4. SessionService Tests

### SessionService.check_session_expiry()

**TC-BS-020**: 16시간 경과로 세션 만료
- Given: 16시간 전에 생성된 세션
- When: check_session_expiry() 호출
- Then: True 반환
- Story: 3.3 (가용성)
- Status: ⬜ Not Started

**TC-BS-021**: 마지막 주문 후 2시간 경과로 세션 만료
- Given: 마지막 주문 후 2시간 경과
- When: check_session_expiry() 호출
- Then: True 반환
- Story: 3.3 (가용성)
- Status: ⬜ Not Started

**TC-BS-022**: 세션 만료되지 않음
- Given: 1시간 전에 생성, 30분 전 마지막 주문
- When: check_session_expiry() 호출
- Then: False 반환
- Story: 3.3 (가용성)
- Status: ⬜ Not Started

---

## 5. Repository Tests

### AdminUserRepository.find_by_store_and_username()

**TC-BS-023**: 관리자 조회 성공
- Given: 존재하는 store_id, username
- When: find_by_store_and_username() 호출
- Then: AdminUser 객체 반환
- Story: 3.1 (성능)
- Status: ⬜ Not Started

**TC-BS-024**: 관리자 조회 실패 (존재하지 않음)
- Given: 존재하지 않는 username
- When: find_by_store_and_username() 호출
- Then: None 반환
- Story: 3.1 (성능)
- Status: ⬜ Not Started

### OrderRepository.find_by_session()

**TC-BS-025**: 세션의 주문 목록 조회
- Given: 세션 ID
- When: find_by_session() 호출
- Then: 주문 목록 반환 (시간 역순)
- Story: 3.1 (성능)
- Status: ⬜ Not Started

---

## 6. API Endpoint Tests

### POST /api/auth/admin-login

**TC-BS-026**: 관리자 로그인 API 성공
- Given: 유효한 요청 body
- When: POST /api/auth/admin-login
- Then: 200 OK, JWT 토큰 반환
- Story: 3.2 (보안)
- Status: ⬜ Not Started

**TC-BS-027**: 관리자 로그인 API 실패 (잘못된 비밀번호)
- Given: 잘못된 password
- When: POST /api/auth/admin-login
- Then: 401 Unauthorized
- Story: 3.2 (보안)
- Status: ⬜ Not Started

### POST /api/orders

**TC-BS-028**: 주문 생성 API 성공
- Given: 유효한 세션 토큰, 주문 아이템
- When: POST /api/orders
- Then: 201 Created, Order 객체 반환
- Story: 3.1 (성능)
- Status: ⬜ Not Started

**TC-BS-029**: 주문 생성 API 응답 시간 (성능)
- Given: 유효한 요청
- When: POST /api/orders
- Then: 응답 시간 500ms 이하
- Story: 3.1 (성능)
- Status: ⬜ Not Started

### GET /api/admin/sse/orders

**TC-BS-030**: SSE 연결 성공
- Given: 유효한 JWT 토큰
- When: GET /api/admin/sse/orders
- Then: SSE 스트림 연결
- Story: 3.1 (성능)
- Status: ⬜ Not Started

**TC-BS-031**: SSE 실시간 업데이트 (2초 이내)
- Given: SSE 연결 중
- When: 새 주문 생성
- Then: 2초 이내에 이벤트 수신
- Story: 3.1 (성능)
- Status: ⬜ Not Started

---

## 7. Utility Tests

### SecurityUtils.hash_password()

**TC-BS-032**: 비밀번호 해싱 (bcrypt)
- Given: 평문 비밀번호
- When: hash_password() 호출
- Then: bcrypt 해시 반환
- Story: 3.2 (보안)
- Status: ⬜ Not Started

### SecurityUtils.verify_password()

**TC-BS-033**: 비밀번호 검증 성공
- Given: 평문 비밀번호, 올바른 해시
- When: verify_password() 호출
- Then: True 반환
- Story: 3.2 (보안)
- Status: ⬜ Not Started

### SessionUtils.calculate_expiry_time()

**TC-BS-034**: 세션 만료 시간 계산 (16시간 우선)
- Given: created_at, last_order_at=None
- When: calculate_expiry_time() 호출
- Then: created_at + 16시간 반환
- Story: 3.3 (가용성)
- Status: ⬜ Not Started

**TC-BS-035**: 세션 만료 시간 계산 (마지막 주문 후 2시간 우선)
- Given: created_at (1시간 전), last_order_at (30분 전)
- When: calculate_expiry_time() 호출
- Then: last_order_at + 2시간 반환 (16시간보다 먼저)
- Story: 3.3 (가용성)
- Status: ⬜ Not Started

---

## 8. Integration Tests

### 주문 생성 플로우 (End-to-End)

**TC-BS-036**: 테이블 로그인 → 주문 생성 → 주문 조회
- Given: 유효한 테이블 인증 정보
- When: 로그인 → 주문 생성 → 주문 조회
- Then: 모든 단계 성공, 주문 내역 확인
- Story: 3.1, 3.2, 3.3
- Status: ⬜ Not Started

---

## Requirements Coverage

| Requirement ID | Test Cases | Status |
|---------------|------------|--------|
| REQ-PERF-001 (API 응답 500ms) | TC-BS-029 | ⬜ Pending |
| REQ-PERF-002 (실시간 2초) | TC-BS-031 | ⬜ Pending |
| REQ-SEC-001 (JWT 인증) | TC-BS-001, TC-BS-007, TC-BS-026 | ⬜ Pending |
| REQ-SEC-002 (bcrypt 해싱) | TC-BS-032, TC-BS-033 | ⬜ Pending |
| REQ-SEC-003 (로그인 제한) | TC-BS-003, TC-BS-004, TC-BS-006 | ⬜ Pending |
| REQ-SEC-004 (권한 검증) | TC-BS-027 | ⬜ Pending |
| REQ-SEC-005 (SQL Injection) | (ORM 사용으로 자동 방어) | ⬜ Pending |
| REQ-AVAIL-001 (에러 로깅) | (모든 테스트에서 검증) | ⬜ Pending |
| REQ-AVAIL-002 (세션 만료) | TC-BS-010, TC-BS-020, TC-BS-021 | ⬜ Pending |
| REQ-AVAIL-003 (에러 메시지) | TC-BS-002, TC-BS-013, TC-BS-016 | ⬜ Pending |

---

## Test Summary

**Total Test Cases**: 36개  
**By Story**:
- Story 3.1 (성능): 10개
- Story 3.2 (보안): 18개
- Story 3.3 (가용성): 8개

**By Layer**:
- Service Layer: 15개
- Repository Layer: 3개
- API Layer: 6개
- Utility Layer: 4개
- Integration: 1개
- Models: 7개 (implicit)

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
