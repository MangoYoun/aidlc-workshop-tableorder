# Build Instructions

## Prerequisites

### 필수 도구
- **Python**: 3.9 이상
- **pip**: Python 패키지 관리자
- **PostgreSQL**: 13 이상
- **Git**: 버전 관리

### 시스템 요구사항
- **OS**: Windows, macOS, Linux
- **Memory**: 최소 2GB RAM
- **Disk Space**: 최소 500MB

---

## Build Steps

### 1. 저장소 클론 (이미 완료된 경우 생략)

```bash
# 이미 workspace에 있으므로 생략
cd <workspace-root>
```

### 2. Python 가상 환경 생성 (권장)

```bash
# Windows (cmd)
python -m venv venv
venv\Scripts\activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 의존성 설치

```bash
pip install -r config/requirements.txt
```

**설치되는 패키지** (총 13개):
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- sqlalchemy==2.0.23
- psycopg2-binary==2.9.9
- python-jose[cryptography]==3.3.0
- passlib[bcrypt]==1.7.4
- python-dotenv==1.0.0
- pydantic==2.5.0
- pydantic-settings==2.1.0
- pytest==7.4.3
- pytest-asyncio==0.21.1
- httpx==0.25.1
- alembic==1.12.1

### 4. 환경 변수 설정

```bash
# .env 파일 생성
copy config\.env.example .env

# .env 파일 편집 (필수 값 입력)
# - DATABASE_URL: PostgreSQL 연결 URL
# - JWT_SECRET_KEY: JWT 서명 키 (랜덤 문자열)
```

**필수 환경 변수**:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/tableorder
JWT_SECRET_KEY=your-secret-key-here-change-in-production
JWT_EXPIRE_HOURS=16
SESSION_EXPIRE_HOURS=16
SESSION_LAST_ORDER_TIMEOUT_HOURS=2
ENVIRONMENT=development
FRONTEND_URL=http://localhost:3000
LOG_LEVEL=INFO
```

### 5. Database 생성

```bash
# PostgreSQL에 접속하여 데이터베이스 생성
psql -U postgres

# PostgreSQL 프롬프트에서
CREATE DATABASE tableorder;
\q
```

### 6. Database 마이그레이션 (현재는 자동 생성)

현재 코드는 `src/database.py`에서 `Base.metadata.create_all()`을 사용하여 자동으로 테이블을 생성합니다.

**향후 Alembic 마이그레이션 사용 시**:
```bash
# Alembic 초기화 (향후)
alembic init alembic

# 마이그레이션 생성 (향후)
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 실행 (향후)
alembic upgrade head
```

### 7. 빌드 검증

Python은 컴파일 언어가 아니므로 별도의 빌드 과정이 없습니다. 대신 Syntax 검증을 수행합니다:

```bash
# Python Syntax 검증
python -m py_compile src/main.py
python -m py_compile src/models.py
python -m py_compile src/services.py
python -m py_compile src/utils.py
python -m py_compile src/config.py
python -m py_compile src/database.py
```

**예상 출력**: 에러 없이 완료되면 성공

### 8. 서버 실행 테스트

```bash
# 개발 서버 실행
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**예상 출력**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 9. Health Check 확인

브라우저 또는 curl로 Health Check 엔드포인트 확인:

```bash
curl http://localhost:8000/health
```

**예상 응답**:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-09T..."
}
```

### 10. API 문서 확인

브라우저에서 Swagger UI 확인:
- http://localhost:8000/docs

**예상 결과**: 12개 API 엔드포인트가 표시됨

---

## Build Artifacts

빌드 후 생성되는 아티팩트:

1. **Python Bytecode** (자동 생성):
   - `src/__pycache__/*.pyc`
   - `tests/__pycache__/*.pyc`

2. **Database Tables** (자동 생성):
   - stores
   - admin_users
   - table_auths
   - table_sessions
   - categories
   - menus
   - orders
   - order_items

3. **Log Files** (실행 시 생성):
   - `logs/app.log` (설정 시)

---

## Troubleshooting

### 1. 의존성 설치 실패

**증상**: `pip install` 실패

**원인**:
- pip 버전이 오래됨
- 네트워크 문제
- 컴파일러 누락 (psycopg2-binary 설치 시)

**해결**:
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 개별 패키지 설치 시도
pip install fastapi
pip install sqlalchemy
# ...
```

### 2. PostgreSQL 연결 실패

**증상**: `sqlalchemy.exc.OperationalError: could not connect to server`

**원인**:
- PostgreSQL 서버가 실행되지 않음
- DATABASE_URL이 잘못됨
- 방화벽 차단

**해결**:
```bash
# PostgreSQL 서비스 상태 확인 (Windows)
sc query postgresql-x64-13

# PostgreSQL 서비스 시작 (Windows)
net start postgresql-x64-13

# 연결 테스트
psql -U postgres -h localhost -p 5432
```

### 3. JWT_SECRET_KEY 누락

**증상**: `KeyError: 'JWT_SECRET_KEY'`

**원인**: .env 파일에 JWT_SECRET_KEY가 없음

**해결**:
```bash
# .env 파일에 추가
echo JWT_SECRET_KEY=your-random-secret-key-here >> .env
```

### 4. Port 8000 이미 사용 중

**증상**: `OSError: [Errno 98] Address already in use`

**원인**: 다른 프로세스가 8000 포트 사용 중

**해결**:
```bash
# Windows: 포트 사용 프로세스 확인
netstat -ano | findstr :8000

# 프로세스 종료
taskkill /PID <PID> /F

# 또는 다른 포트 사용
uvicorn src.main:app --reload --port 8001
```

### 5. Import 에러

**증상**: `ModuleNotFoundError: No module named 'src'`

**원인**: Python 경로 문제

**해결**:
```bash
# workspace root에서 실행 확인
cd <workspace-root>

# PYTHONPATH 설정 (Windows cmd)
set PYTHONPATH=%CD%

# PYTHONPATH 설정 (Windows PowerShell)
$env:PYTHONPATH = $PWD

# 또는 -m 옵션 사용
python -m uvicorn src.main:app --reload
```

---

## Build Success Criteria

✅ 모든 의존성 설치 완료  
✅ .env 파일 설정 완료  
✅ Database 연결 성공  
✅ Python Syntax 검증 통과  
✅ 서버 실행 성공  
✅ Health Check 응답 정상  
✅ API 문서 접근 가능  

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
