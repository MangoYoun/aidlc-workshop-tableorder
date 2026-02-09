# TDD Code Generation Plan for Backend Service

## Unit Context

**Workspace Root**: Workspace root (Greenfield single unit)  
**Project Type**: Greenfield  
**Project Structure**: `src/`, `tests/`, `config/` in workspace root

**Stories to Implement**:
- Story 3.1: 성능 요구사항
- Story 3.2: 보안 요구사항
- Story 3.3: 가용성 요구사항

**Total Test Cases**: 36개  
**Estimated Steps**: 약 150개 (Step 0 + 각 메서드마다 RED-GREEN-REFACTOR)

---

## Plan Step 0: Project Structure & Contract Skeleton Generation

- [x] 프로젝트 디렉토리 구조 생성
- [x] 의존성 파일 생성 (requirements.txt)
- [x] 환경 설정 파일 생성 (.env.example, config.py)
- [x] Database 설정 파일 생성 (database.py)
- [x] 모든 Contract 클래스/인터페이스 Skeleton 생성
- [x] 모든 메서드 완전 구현 (Fast Track 방식)
- [x] 컴파일/Syntax 검증

**Output**:
```
src/
├── models/
│   ├── __init__.py
│   ├── store.py (Store skeleton)
│   ├── admin_user.py (AdminUser skeleton)
│   ├── table_auth.py (TableAuth skeleton)
│   ├── table_session.py (TableSession skeleton)
│   ├── category.py (Category skeleton)
│   ├── menu.py (Menu skeleton)
│   ├── order.py (Order skeleton)
│   └── order_item.py (OrderItem skeleton)
├── repositories/
│   ├── __init__.py
│   ├── admin_user_repository.py (skeleton)
│   ├── table_auth_repository.py (skeleton)
│   ├── table_session_repository.py (skeleton)
│   ├── menu_repository.py (skeleton)
│   └── order_repository.py (skeleton)
├── services/
│   ├── __init__.py
│   ├── auth_service.py (skeleton)
│   ├── menu_service.py (skeleton)
│   ├── order_service.py (skeleton)
│   └── session_service.py (skeleton)
├── api/
│   ├── __init__.py
│   ├── auth_routes.py (skeleton)
│   ├── menu_routes.py (skeleton)
│   ├── order_routes.py (skeleton)
│   └── sse_routes.py (skeleton)
├── utils/
│   ├── __init__.py
│   ├── security_utils.py (skeleton)
│   └── session_utils.py (skeleton)
├── middleware/
│   ├── __init__.py
│   ├── timing_middleware.py (skeleton)
│   └── auth_middleware.py (skeleton)
├── database.py
├── config.py
└── main.py

tests/
├── __init__.py
├── test_auth_service.py (empty)
├── test_menu_service.py (empty)
├── test_order_service.py (empty)
├── test_session_service.py (empty)
├── test_repositories.py (empty)
├── test_api_endpoints.py (empty)
└── test_utils.py (empty)

config/
├── .env.example
└── requirements.txt
```

---

## Plan Step 1: Models Layer (TDD)

### 1.1 Store Model
- [ ] Store - RED-GREEN-REFACTOR
  - [ ] RED: 테스트 작성 (Store 생성, 필드 검증)
  - [ ] GREEN: 최소 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: 모든 테스트 통과

### 1.2 AdminUser Model
- [ ] AdminUser - RED-GREEN-REFACTOR
  - [ ] RED: 테스트 작성 (TC-BS-023 관련)
  - [ ] GREEN: 최소 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: 모든 테스트 통과

### 1.3 TableAuth Model
- [ ] TableAuth - RED-GREEN-REFACTOR
  - [ ] RED: 테스트 작성
  - [ ] GREEN: 최소 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: 모든 테스트 통과

### 1.4 TableSession Model
- [ ] TableSession - RED-GREEN-REFACTOR
  - [ ] RED: 테스트 작성
  - [ ] GREEN: 최소 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: 모든 테스트 통과

### 1.5 Category, Menu, Order, OrderItem Models
- [ ] Category - RED-GREEN-REFACTOR
- [ ] Menu - RED-GREEN-REFACTOR
- [ ] Order - RED-GREEN-REFACTOR
- [ ] OrderItem - RED-GREEN-REFACTOR

**Story**: 3.2 (보안 - 데이터 모델 무결성)

---

## Plan Step 2: Utility Layer (TDD)

### 2.1 SecurityUtils.hash_password()
- [ ] SecurityUtils.hash_password() - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-032 작성 및 실패 확인
  - [ ] GREEN: bcrypt 해싱 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: TC-BS-032 통과

### 2.2 SecurityUtils.verify_password()
- [ ] SecurityUtils.verify_password() - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-033 작성 및 실패 확인
  - [ ] GREEN: bcrypt 검증 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: TC-BS-033 통과

### 2.3 SecurityUtils.create_jwt_token()
- [ ] SecurityUtils.create_jwt_token() - RED-GREEN-REFACTOR
  - [ ] RED: 테스트 작성 및 실패 확인
  - [ ] GREEN: JWT 생성 구현 (python-jose)
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: 테스트 통과

### 2.4 SecurityUtils.verify_jwt_token()
- [ ] SecurityUtils.verify_jwt_token() - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-007, TC-BS-008 작성 및 실패 확인
  - [ ] GREEN: JWT 검증 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: TC-BS-007, TC-BS-008 통과

### 2.5 SessionUtils.generate_session_token()
- [ ] SessionUtils.generate_session_token() - RED-GREEN-REFACTOR
  - [ ] RED: 테스트 작성 및 실패 확인
  - [ ] GREEN: UUID 생성 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: 테스트 통과

### 2.6 SessionUtils.calculate_expiry_time()
- [ ] SessionUtils.calculate_expiry_time() - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-034, TC-BS-035 작성 및 실패 확인
  - [ ] GREEN: 만료 시간 계산 로직 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: TC-BS-034, TC-BS-035 통과

**Story**: 3.2 (보안), 3.3 (가용성)

---

## Plan Step 3: Repository Layer (TDD)

### 3.1 AdminUserRepository.find_by_store_and_username()
- [ ] AdminUserRepository.find_by_store_and_username() - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-023, TC-BS-024 작성 및 실패 확인
  - [ ] GREEN: SQLAlchemy 쿼리 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: TC-BS-023, TC-BS-024 통과

### 3.2 AdminUserRepository.save()
- [ ] AdminUserRepository.save() - RED-GREEN-REFACTOR
  - [ ] RED: 테스트 작성 및 실패 확인
  - [ ] GREEN: INSERT/UPDATE 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: 테스트 통과

### 3.3 AdminUserRepository.update_login_attempts()
- [ ] AdminUserRepository.update_login_attempts() - RED-GREEN-REFACTOR
  - [ ] RED: 테스트 작성 및 실패 확인
  - [ ] GREEN: UPDATE 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: 테스트 통과

### 3.4 TableAuthRepository (3 methods)
- [ ] TableAuthRepository.find_by_store_and_table_number() - RED-GREEN-REFACTOR
- [ ] TableAuthRepository.save() - RED-GREEN-REFACTOR
- [ ] TableAuthRepository.update_login_attempts() - RED-GREEN-REFACTOR

### 3.5 TableSessionRepository (5 methods)
- [ ] TableSessionRepository.find_by_token() - RED-GREEN-REFACTOR
- [ ] TableSessionRepository.find_active_by_table_auth() - RED-GREEN-REFACTOR
- [ ] TableSessionRepository.save() - RED-GREEN-REFACTOR
- [ ] TableSessionRepository.update_last_order_time() - RED-GREEN-REFACTOR
- [ ] TableSessionRepository.close_session() - RED-GREEN-REFACTOR

### 3.6 MenuRepository (4 methods)
- [ ] MenuRepository.find_by_store() - RED-GREEN-REFACTOR
- [ ] MenuRepository.find_by_id() - RED-GREEN-REFACTOR
- [ ] MenuRepository.save() - RED-GREEN-REFACTOR
- [ ] MenuRepository.delete() - RED-GREEN-REFACTOR

### 3.7 OrderRepository (4 methods)
- [ ] OrderRepository.find_by_session() - RED-GREEN-REFACTOR (TC-BS-025)
- [ ] OrderRepository.find_by_store_and_status() - RED-GREEN-REFACTOR
- [ ] OrderRepository.save() - RED-GREEN-REFACTOR
- [ ] OrderRepository.update_status() - RED-GREEN-REFACTOR

**Story**: 3.1 (성능 - 쿼리 최적화)

---

## Plan Step 4: Service Layer - AuthService (TDD)

### 4.1 AuthService.login_admin()
- [ ] AuthService.login_admin() - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-001 작성 및 실패 확인
  - [ ] GREEN: 최소 구현 (인증 성공 케이스만)
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: TC-BS-001 통과
  - [ ] RED: TC-BS-002 작성 및 실패 확인
  - [ ] GREEN: 비밀번호 검증 추가
  - [ ] VERIFY: TC-BS-001, TC-BS-002 통과
  - [ ] RED: TC-BS-003 작성 및 실패 확인
  - [ ] GREEN: 로그인 시도 제한 로직 추가
  - [ ] VERIFY: TC-BS-001~003 통과
  - [ ] RED: TC-BS-004 작성 및 실패 확인
  - [ ] GREEN: 계정 잠금 체크 추가
  - [ ] REFACTOR: 최종 코드 개선
  - [ ] VERIFY: TC-BS-001~004 모두 통과

### 4.2 AuthService.login_table()
- [ ] AuthService.login_table() - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-005 작성 및 실패 확인
  - [ ] GREEN: 최소 구현
  - [ ] RED: TC-BS-006 작성 및 실패 확인
  - [ ] GREEN: 로그인 제한 추가
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: TC-BS-005, TC-BS-006 통과

### 4.3 AuthService.verify_jwt_token()
- [ ] AuthService.verify_jwt_token() - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-007, TC-BS-008 작성 및 실패 확인
  - [ ] GREEN: JWT 검증 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: TC-BS-007, TC-BS-008 통과

### 4.4 AuthService.verify_session_token()
- [ ] AuthService.verify_session_token() - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-009, TC-BS-010 작성 및 실패 확인
  - [ ] GREEN: 세션 검증 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: TC-BS-009, TC-BS-010 통과

**Story**: 3.2 (보안), 3.3 (가용성)

---

## Plan Step 5: Service Layer - MenuService (TDD)

### 5.1 MenuService.get_menus_by_store()
- [ ] MenuService.get_menus_by_store() - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-011 작성 및 실패 확인
  - [ ] GREEN: 메뉴 조회 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: TC-BS-011 통과

### 5.2 MenuService.create_menu()
- [ ] MenuService.create_menu() - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-012, TC-BS-013 작성 및 실패 확인
  - [ ] GREEN: 메뉴 생성 및 검증 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: TC-BS-012, TC-BS-013 통과

### 5.3 MenuService.update_menu()
- [ ] MenuService.update_menu() - RED-GREEN-REFACTOR

### 5.4 MenuService.delete_menu()
- [ ] MenuService.delete_menu() - RED-GREEN-REFACTOR

**Story**: 3.1 (성능), 3.2 (보안)

---

## Plan Step 6: Service Layer - OrderService (TDD)

### 6.1 OrderService.create_order()
- [ ] OrderService.create_order() - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-014 작성 및 실패 확인
  - [ ] GREEN: 최소 구현
  - [ ] RED: TC-BS-015 작성 및 실패 확인
  - [ ] GREEN: 세션 만료 체크 추가
  - [ ] RED: TC-BS-016 작성 및 실패 확인
  - [ ] GREEN: 수량 검증 추가
  - [ ] RED: TC-BS-017 작성 및 실패 확인
  - [ ] GREEN: last_order_at 업데이트 추가
  - [ ] REFACTOR: 최종 코드 개선
  - [ ] VERIFY: TC-BS-014~017 모두 통과

### 6.2 OrderService.get_orders_by_session()
- [ ] OrderService.get_orders_by_session() - RED-GREEN-REFACTOR

### 6.3 OrderService.update_order_status()
- [ ] OrderService.update_order_status() - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-018, TC-BS-019 작성 및 실패 확인
  - [ ] GREEN: 상태 전이 검증 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: TC-BS-018, TC-BS-019 통과

**Story**: 3.1 (성능), 3.2 (보안), 3.3 (가용성)

---

## Plan Step 7: Service Layer - SessionService (TDD)

### 7.1 SessionService.check_session_expiry()
- [ ] SessionService.check_session_expiry() - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-020, TC-BS-021, TC-BS-022 작성 및 실패 확인
  - [ ] GREEN: 세션 만료 로직 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: TC-BS-020~022 통과

### 7.2 SessionService.close_session()
- [ ] SessionService.close_session() - RED-GREEN-REFACTOR

**Story**: 3.3 (가용성)

---

## Plan Step 8: API Layer - Auth Endpoints (TDD)

### 8.1 POST /api/auth/admin-login
- [ ] POST /api/auth/admin-login - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-026, TC-BS-027 작성 및 실패 확인
  - [ ] GREEN: 엔드포인트 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: TC-BS-026, TC-BS-027 통과

### 8.2 POST /api/auth/table-login
- [ ] POST /api/auth/table-login - RED-GREEN-REFACTOR

**Story**: 3.2 (보안)

---

## Plan Step 9: API Layer - Menu Endpoints (TDD)

### 9.1 GET /api/menus
- [ ] GET /api/menus - RED-GREEN-REFACTOR

### 9.2 POST /api/admin/menus
- [ ] POST /api/admin/menus - RED-GREEN-REFACTOR

### 9.3 PUT /api/admin/menus/{menu_id}
- [ ] PUT /api/admin/menus/{menu_id} - RED-GREEN-REFACTOR

### 9.4 DELETE /api/admin/menus/{menu_id}
- [ ] DELETE /api/admin/menus/{menu_id} - RED-GREEN-REFACTOR

**Story**: 3.1 (성능), 3.2 (보안)

---

## Plan Step 10: API Layer - Order Endpoints (TDD)

### 10.1 POST /api/orders
- [ ] POST /api/orders - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-028, TC-BS-029 작성 및 실패 확인
  - [ ] GREEN: 엔드포인트 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: TC-BS-028, TC-BS-029 통과 (응답 시간 500ms 이하)

### 10.2 GET /api/orders
- [ ] GET /api/orders - RED-GREEN-REFACTOR

### 10.3 GET /api/admin/orders
- [ ] GET /api/admin/orders - RED-GREEN-REFACTOR

### 10.4 PUT /api/admin/orders/{order_id}/status
- [ ] PUT /api/admin/orders/{order_id}/status - RED-GREEN-REFACTOR

**Story**: 3.1 (성능)

---

## Plan Step 11: API Layer - SSE Endpoint (TDD)

### 11.1 GET /api/admin/sse/orders
- [ ] GET /api/admin/sse/orders - RED-GREEN-REFACTOR
  - [ ] RED: TC-BS-030, TC-BS-031 작성 및 실패 확인
  - [ ] GREEN: SSE 스트림 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: TC-BS-030, TC-BS-031 통과 (2초 이내 업데이트)

**Story**: 3.1 (성능)

---

## Plan Step 12: Middleware Layer (TDD)

### 12.1 TimingMiddleware
- [ ] TimingMiddleware - RED-GREEN-REFACTOR
  - [ ] RED: 테스트 작성 (응답 시간 측정, 500ms 초과 시 WARNING)
  - [ ] GREEN: Middleware 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: 테스트 통과

### 12.2 AuthMiddleware
- [ ] AuthMiddleware - RED-GREEN-REFACTOR
  - [ ] RED: 테스트 작성 (/api/admin/* 경로 체크)
  - [ ] GREEN: Middleware 구현
  - [ ] REFACTOR: 코드 개선
  - [ ] VERIFY: 테스트 통과

**Story**: 3.1 (성능), 3.2 (보안)

---

## Plan Step 13: Integration Tests (TDD)

### 13.1 End-to-End 주문 플로우
- [ ] TC-BS-036 - RED-GREEN-REFACTOR
  - [ ] RED: 테스트 작성 (로그인 → 주문 생성 → 조회)
  - [ ] GREEN: 통합 테스트 통과 확인
  - [ ] REFACTOR: 테스트 코드 개선
  - [ ] VERIFY: TC-BS-036 통과

**Story**: 3.1, 3.2, 3.3

---

## Plan Step 14: Database Migration Scripts

- [ ] Alembic 초기화
- [ ] 마이그레이션 스크립트 생성 (8개 테이블)
- [ ] 인덱스 생성 스크립트
- [ ] 마이그레이션 테스트

**Story**: 3.1 (성능 - 인덱스)

---

## Plan Step 15: Documentation & Deployment Artifacts

- [ ] API 문서 생성 (FastAPI 자동 생성 + 추가 설명)
- [ ] README.md 업데이트
- [ ] requirements.txt 최종 확인
- [ ] .env.example 최종 확인
- [ ] Deployment 가이드 생성

**Story**: 3.3 (가용성)

---

## TDD Execution Summary

**Total Plan Steps**: 15개  
**Total Methods to Implement**: 약 50개  
**Total Test Cases**: 36개  
**Estimated RED-GREEN-REFACTOR Cycles**: 약 50회

**Story Coverage**:
- Story 3.1 (성능): Plan Steps 1, 3, 5, 6, 9, 10, 11, 12, 14
- Story 3.2 (보안): Plan Steps 1, 2, 4, 5, 6, 8, 9, 12
- Story 3.3 (가용성): Plan Steps 2, 4, 6, 7, 13, 15

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
