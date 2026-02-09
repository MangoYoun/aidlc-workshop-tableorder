# Unit Test Execution

## TDD 방식 사용 확인

✅ **TDD 아티팩트 발견**:
- `aidlc-docs/construction/plans/backend-service-test-plan.md`
- `aidlc-docs/construction/plans/backend-service-contracts.md`
- `aidlc-docs/construction/plans/backend-service-tdd-code-generation-plan.md`

**TDD 방식으로 코드 생성됨**: Unit tests는 이미 Code Generation 단계에서 실행되었습니다.

**현재 상태**: Fast Track 방식으로 코드 생성 완료, 테스트 Skeleton만 생성됨

---

## Unit Test Overview

### Test Plan 참조

상세한 테스트 케이스는 다음 문서를 참조하세요:
- **Test Plan**: `aidlc-docs/construction/plans/backend-service-test-plan.md`
- **Contracts**: `aidlc-docs/construction/plans/backend-service-contracts.md`

**총 테스트 케이스**: 36개
- AuthService: 10개 (TC-BS-001 ~ TC-BS-010)
- MenuService: 3개 (TC-BS-011 ~ TC-BS-013)
- OrderService: 6개 (TC-BS-014 ~ TC-BS-019)
- SessionService: 3개 (TC-BS-020 ~ TC-BS-022)
- Repositories: 2개 (TC-BS-023 ~ TC-BS-024)
- Orders Query: 1개 (TC-BS-025)
- API Endpoints: 4개 (TC-BS-026 ~ TC-BS-029)
- SSE: 2개 (TC-BS-030 ~ TC-BS-031)
- Security: 2개 (TC-BS-032 ~ TC-BS-033)
- Session Expiry: 2개 (TC-BS-034 ~ TC-BS-035)
- Integration: 1개 (TC-BS-036)

---

## Test Environment Setup

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

### 3. pytest 설정 확인

`pytest.ini` 파일 생성 (workspace root):

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
```

---

## Run Unit Tests

### 1. 전체 테스트 실행

```bash
# 모든 테스트 실행
pytest tests/ -v

# 또는 특정 파일만
pytest tests/test_services.py -v
```

**예상 출력**:
```
tests/test_services.py::test_auth_service_login_admin PASSED
tests/test_services.py::test_menu_service_get_menus PASSED
tests/test_services.py::test_order_service_create_order PASSED
tests/test_services.py::test_session_service_check_expiry PASSED
tests/test_services.py::test_security_utils_hash_password PASSED

======================== X passed in Y.YYs ========================
```

### 2. 커버리지 측정

```bash
# pytest-cov 설치 (필요시)
pip install pytest-cov

# 커버리지 측정
pytest tests/ --cov=src --cov-report=html --cov-report=term

# 커버리지 리포트 확인
# htmlcov/index.html 파일을 브라우저로 열기
```

**목표 커버리지**: 80% 이상

### 3. 특정 테스트 케이스 실행

```bash
# 특정 테스트 함수만 실행
pytest tests/test_services.py::test_auth_service_login_admin -v

# 특정 클래스만 실행
pytest tests/test_services.py::TestAuthService -v

# 키워드로 필터링
pytest tests/ -k "auth" -v
```

---

## Test Implementation Status

### 현재 상태 (Fast Track 방식)

**생성된 파일**: `tests/test_services.py`

**구현된 테스트**: 5개 Skeleton
- `test_auth_service_login_admin()` - Skeleton
- `test_menu_service_get_menus()` - Skeleton
- `test_order_service_create_order()` - Skeleton
- `test_session_service_check_expiry()` - Skeleton
- `test_security_utils_hash_password()` - Skeleton

**미구현 테스트**: 31개 (TC-BS-002 ~ TC-BS-036)

### 테스트 구현 우선순위

#### Priority 1: 핵심 기능 (필수)

1. **AuthService** (TC-BS-001 ~ TC-BS-010):
   - 관리자 로그인 성공/실패
   - 테이블 로그인 성공/실패
   - JWT 검증
   - 세션 토큰 검증

2. **OrderService** (TC-BS-014 ~ TC-BS-019):
   - 주문 생성 성공/실패
   - 세션 만료 체크
   - 주문 상태 전이 검증

3. **SessionService** (TC-BS-020 ~ TC-BS-022):
   - 세션 만료 체크 (16시간)
   - 마지막 주문 후 타임아웃 (2시간)

#### Priority 2: 보안 및 성능 (중요)

4. **Security Utils** (TC-BS-032 ~ TC-BS-033):
   - 비밀번호 해싱
   - 비밀번호 검증

5. **API Endpoints** (TC-BS-026 ~ TC-BS-029):
   - 관리자 로그인 API
   - 주문 생성 API (응답 시간 500ms 이하)

6. **SSE** (TC-BS-030 ~ TC-BS-031):
   - SSE 스트림 연결
   - 주문 업데이트 전송 (2초 이내)

#### Priority 3: 추가 기능 (선택)

7. **MenuService** (TC-BS-011 ~ TC-BS-013):
   - 메뉴 조회
   - 메뉴 생성 및 검증

8. **Repositories** (TC-BS-023 ~ TC-BS-025):
   - AdminUser 조회
   - Order 조회

---

## Test Implementation Guide

### 테스트 작성 예시

**TC-BS-001: 관리자 로그인 성공**

```python
import pytest
from src.services import AuthService
from src.models import Store, AdminUser
from src.database import get_db

@pytest.mark.asyncio
async def test_auth_service_login_admin_success():
    """TC-BS-001: 관리자 로그인 성공"""
    # Given: 유효한 관리자 계정이 존재
    db = next(get_db())
    store = Store(name="Test Store")
    db.add(store)
    db.commit()
    
    admin = AdminUser(
        store_id=store.id,
        username="admin",
        password_hash="hashed_password",
        role="ADMIN"
    )
    db.add(admin)
    db.commit()
    
    # When: 올바른 자격증명으로 로그인
    auth_service = AuthService(db)
    result = await auth_service.login_admin(
        store_id=store.id,
        username="admin",
        password="correct_password"
    )
    
    # Then: JWT 토큰 반환
    assert result is not None
    assert "access_token" in result
    assert result["token_type"] == "bearer"
```

### 테스트 Fixture 예시

```python
import pytest
from src.database import Base, engine, get_db

@pytest.fixture(scope="function")
def test_db():
    """테스트용 Database Fixture"""
    # Setup: 테이블 생성
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    
    yield db
    
    # Teardown: 테이블 삭제
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_store(test_db):
    """샘플 Store Fixture"""
    store = Store(name="Test Store")
    test_db.add(store)
    test_db.commit()
    return store
```

---

## Test Execution Checklist

### 실행 전 체크리스트

- [ ] Test Database 생성 완료
- [ ] .env.test 파일 설정 완료
- [ ] pytest 설치 완료
- [ ] 가상 환경 활성화 완료

### 실행 후 체크리스트

- [ ] 모든 테스트 통과 (0 failures)
- [ ] 커버리지 80% 이상
- [ ] 성능 테스트 통과 (TC-BS-029: 500ms 이하)
- [ ] 보안 테스트 통과 (TC-BS-032, TC-BS-033)
- [ ] 테스트 리포트 생성 완료

---

## Troubleshooting

### 1. Database 연결 실패

**증상**: `sqlalchemy.exc.OperationalError`

**해결**:
```bash
# Test Database 존재 확인
psql -U postgres -c "\l" | findstr tableorder_test

# .env.test 파일 확인
type .env.test
```

### 2. Import 에러

**증상**: `ModuleNotFoundError: No module named 'src'`

**해결**:
```bash
# PYTHONPATH 설정
set PYTHONPATH=%CD%

# 또는 pytest 실행 시
python -m pytest tests/ -v
```

### 3. Async 테스트 실패

**증상**: `RuntimeError: Event loop is closed`

**해결**:
```bash
# pytest-asyncio 설치 확인
pip install pytest-asyncio

# pytest.ini에 asyncio_mode 설정 확인
```

### 4. Fixture 에러

**증상**: `fixture 'test_db' not found`

**해결**:
- `conftest.py` 파일에 Fixture 정의
- Fixture scope 확인 (function, class, module, session)

---

## Test Report Location

테스트 실행 후 생성되는 리포트:

1. **터미널 출력**: 실시간 테스트 결과
2. **Coverage HTML**: `htmlcov/index.html`
3. **JUnit XML** (CI/CD용):
   ```bash
   pytest tests/ --junitxml=test-results.xml
   ```

---

## Next Steps

1. **Priority 1 테스트 구현**: AuthService, OrderService, SessionService
2. **테스트 실행 및 검증**: 모든 테스트 통과 확인
3. **커버리지 측정**: 80% 이상 달성
4. **Integration Tests로 진행**: 다음 단계

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
