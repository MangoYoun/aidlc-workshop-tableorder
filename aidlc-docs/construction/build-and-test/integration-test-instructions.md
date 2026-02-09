# Integration Test Instructions

## Purpose

Backend Service Unit의 통합 테스트를 수행하여 컴포넌트 간 상호작용이 올바르게 동작하는지 검증합니다.

---

## Test Scenarios

### Scenario 1: 관리자 로그인 → 메뉴 관리 플로우

**Description**: 관리자가 로그인하여 메뉴를 생성/수정/삭제하는 전체 플로우

**Setup**:
```bash
# Test Database 초기화
psql -U postgres -d tableorder_test -c "TRUNCATE TABLE admin_users, stores, menus, categories CASCADE;"
```

**Test Steps**:
1. Store 생성
2. AdminUser 생성
3. POST /api/auth/admin-login (JWT 토큰 획득)
4. POST /api/admin/menus (메뉴 생성)
5. GET /api/menus (메뉴 조회)
6. PUT /api/admin/menus/{menu_id} (메뉴 수정)
7. DELETE /api/admin/menus/{menu_id} (메뉴 삭제)

**Expected Results**:
- 모든 API 호출 성공 (200/201 응답)
- JWT 토큰이 모든 관리자 API에서 유효
- 메뉴 생성/수정/삭제가 Database에 반영됨

**Cleanup**:
```bash
psql -U postgres -d tableorder_test -c "TRUNCATE TABLE admin_users, stores, menus, categories CASCADE;"
```

---

### Scenario 2: 테이블 로그인 → 주문 생성 플로우

**Description**: 고객이 테이블에 로그인하여 주문을 생성하는 전체 플로우

**Setup**:
```bash
# Test Database 초기화
psql -U postgres -d tableorder_test -c "TRUNCATE TABLE table_auths, table_sessions, orders, order_items CASCADE;"
```

**Test Steps**:
1. Store, TableAuth, Menu 생성
2. POST /api/auth/table-login (세션 토큰 획득)
3. GET /api/menus?store_id={id} (메뉴 조회)
4. POST /api/orders (주문 생성)
5. GET /api/orders (주문 내역 조회)

**Expected Results**:
- 세션 토큰 생성 성공
- 주문 생성 시 last_order_at 업데이트
- 주문 내역 조회 시 현재 세션의 주문만 반환

**Cleanup**:
```bash
psql -U postgres -d tableorder_test -c "TRUNCATE TABLE table_auths, table_sessions, orders, order_items CASCADE;"
```

---

### Scenario 3: 주문 상태 변경 → SSE 알림 플로우

**Description**: 관리자가 주문 상태를 변경하면 SSE로 실시간 알림이 전송되는 플로우

**Setup**:
```bash
# Test Database 초기화
psql -U postgres -d tableorder_test -c "TRUNCATE TABLE orders, order_items CASCADE;"
```

**Test Steps**:
1. AdminUser, Order 생성
2. GET /api/admin/sse/orders (SSE 연결 시작)
3. PUT /api/admin/orders/{order_id}/status (주문 상태 변경)
4. SSE 스트림에서 업데이트 수신 확인

**Expected Results**:
- SSE 연결 성공
- 주문 상태 변경 후 2초 이내 SSE 이벤트 수신
- 이벤트 데이터에 변경된 주문 정보 포함

**Cleanup**:
```bash
psql -U postgres -d tableorder_test -c "TRUNCATE TABLE orders, order_items CASCADE;"
```

---

### Scenario 4: 세션 만료 체크 플로우

**Description**: 세션 만료 조건 (16시간 OR 마지막 주문 후 2시간)이 올바르게 동작하는지 검증

**Setup**:
```bash
# Test Database 초기화
psql -U postgres -d tableorder_test -c "TRUNCATE TABLE table_sessions CASCADE;"
```

**Test Steps**:
1. TableSession 생성 (created_at: 17시간 전)
2. POST /api/orders (세션 만료 에러 확인)
3. TableSession 생성 (last_order_at: 3시간 전)
4. POST /api/orders (세션 만료 에러 확인)
5. TableSession 생성 (last_order_at: 1시간 전)
6. POST /api/orders (주문 생성 성공 확인)

**Expected Results**:
- 16시간 초과 세션: 401 Unauthorized
- 마지막 주문 후 2시간 초과: 401 Unauthorized
- 유효한 세션: 201 Created

**Cleanup**:
```bash
psql -U postgres -d tableorder_test -c "TRUNCATE TABLE table_sessions CASCADE;"
```

---

## Setup Integration Test Environment

### 1. Test Database 생성

```bash
# PostgreSQL에 접속
psql -U postgres

# Test Database 생성
CREATE DATABASE tableorder_test;
\q
```

### 2. Test 환경 변수 설정

`.env.test` 파일 생성:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/tableorder_test
JWT_SECRET_KEY=test-secret-key
JWT_EXPIRE_HOURS=16
SESSION_EXPIRE_HOURS=16
SESSION_LAST_ORDER_TIMEOUT_HOURS=2
ENVIRONMENT=test
FRONTEND_URL=http://localhost:3000
LOG_LEVEL=DEBUG
```

### 3. Test Server 실행

```bash
# Test 환경으로 서버 실행
set DATABASE_URL=postgresql://user:password@localhost:5432/tableorder_test
uvicorn src.main:app --reload --port 8001
```

---

## Run Integration Tests

### 1. pytest를 사용한 통합 테스트

`tests/test_integration.py` 파일 생성:

```python
import pytest
import httpx
from src.main import app

@pytest.mark.asyncio
async def test_admin_menu_management_flow():
    """Scenario 1: 관리자 로그인 → 메뉴 관리 플로우"""
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        # 1. 관리자 로그인
        login_response = await client.post("/api/auth/admin-login", json={
            "store_id": 1,
            "username": "admin",
            "password": "password"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # 2. 메뉴 생성
        headers = {"Authorization": f"Bearer {token}"}
        menu_response = await client.post("/api/admin/menus", json={
            "store_id": 1,
            "category_id": 1,
            "name": "Test Menu",
            "price": 10000
        }, headers=headers)
        assert menu_response.status_code == 201
        menu_id = menu_response.json()["id"]
        
        # 3. 메뉴 조회
        get_response = await client.get(f"/api/menus?store_id=1")
        assert get_response.status_code == 200
        assert len(get_response.json()) > 0
```

**실행**:
```bash
pytest tests/test_integration.py -v
```

### 2. 수동 테스트 (curl 사용)

**Scenario 1: 관리자 로그인 → 메뉴 관리**

```bash
# 1. 관리자 로그인
curl -X POST http://localhost:8001/api/auth/admin-login \
  -H "Content-Type: application/json" \
  -d "{\"store_id\": 1, \"username\": \"admin\", \"password\": \"password\"}"

# 응답에서 access_token 복사
# TOKEN=<access_token>

# 2. 메뉴 생성
curl -X POST http://localhost:8001/api/admin/menus \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer %TOKEN%" \
  -d "{\"store_id\": 1, \"category_id\": 1, \"name\": \"Test Menu\", \"price\": 10000}"

# 3. 메뉴 조회
curl http://localhost:8001/api/menus?store_id=1
```

**Scenario 2: 테이블 로그인 → 주문 생성**

```bash
# 1. 테이블 로그인
curl -X POST http://localhost:8001/api/auth/table-login \
  -H "Content-Type: application/json" \
  -d "{\"store_id\": 1, \"table_number\": \"T01\", \"password\": \"1234\"}"

# 응답에서 session_token 복사
# SESSION_TOKEN=<session_token>

# 2. 주문 생성
curl -X POST http://localhost:8001/api/orders \
  -H "Content-Type: application/json" \
  -H "X-Session-Token: %SESSION_TOKEN%" \
  -d "{\"items\": [{\"menu_id\": 1, \"quantity\": 2}]}"

# 3. 주문 내역 조회
curl http://localhost:8001/api/orders \
  -H "X-Session-Token: %SESSION_TOKEN%"
```

---

## Verify Service Interactions

### 1. Database 상태 확인

```bash
# 주문 생성 후 Database 확인
psql -U postgres -d tableorder_test -c "SELECT * FROM orders;"
psql -U postgres -d tableorder_test -c "SELECT * FROM order_items;"
psql -U postgres -d tableorder_test -c "SELECT * FROM table_sessions;"
```

### 2. 로그 확인

```bash
# 애플리케이션 로그 확인
type logs\app.log

# 또는 실시간 로그 모니터링
tail -f logs/app.log
```

### 3. API 응답 시간 확인

```bash
# Timing Middleware 로그 확인
# 500ms 초과 시 WARNING 로그 출력 확인
```

---

## Expected Results

### Scenario 1: 관리자 로그인 → 메뉴 관리
- ✅ 관리자 로그인 성공 (JWT 토큰 발급)
- ✅ 메뉴 생성 성공 (201 Created)
- ✅ 메뉴 조회 성공 (200 OK)
- ✅ 메뉴 수정 성공 (200 OK)
- ✅ 메뉴 삭제 성공 (204 No Content)

### Scenario 2: 테이블 로그인 → 주문 생성
- ✅ 테이블 로그인 성공 (세션 토큰 발급)
- ✅ 메뉴 조회 성공 (200 OK)
- ✅ 주문 생성 성공 (201 Created)
- ✅ 주문 내역 조회 성공 (200 OK)
- ✅ last_order_at 업데이트 확인

### Scenario 3: 주문 상태 변경 → SSE 알림
- ✅ SSE 연결 성공
- ✅ 주문 상태 변경 성공 (200 OK)
- ✅ SSE 이벤트 수신 (2초 이내)

### Scenario 4: 세션 만료 체크
- ✅ 16시간 초과 세션 거부 (401 Unauthorized)
- ✅ 마지막 주문 후 2시간 초과 거부 (401 Unauthorized)
- ✅ 유효한 세션 허용 (201 Created)

---

## Logs Location

통합 테스트 실행 중 생성되는 로그:

1. **애플리케이션 로그**: `logs/app.log`
2. **테스트 로그**: pytest 터미널 출력
3. **Database 로그**: PostgreSQL 로그 디렉토리

---

## Cleanup

테스트 완료 후 정리:

```bash
# Test Database 삭제
psql -U postgres -c "DROP DATABASE tableorder_test;"

# Test Server 종료
# Ctrl+C

# Test 환경 변수 제거
del .env.test
```

---

## Troubleshooting

### 1. SSE 연결 실패

**증상**: SSE 스트림 연결 안 됨

**해결**:
- 브라우저 EventSource API 사용
- curl --no-buffer 옵션 사용
- httpx stream 사용

### 2. 세션 토큰 인식 안 됨

**증상**: 401 Unauthorized

**해결**:
- Header 이름 확인 (X-Session-Token)
- 토큰 값 확인 (공백 없이)
- Database에 세션 존재 확인

### 3. Database 트랜잭션 충돌

**증상**: IntegrityError

**해결**:
- 각 테스트 전 Database 초기화
- Fixture에서 rollback 수행
- 테스트 격리 확인

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
