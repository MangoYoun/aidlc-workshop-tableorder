# Local Development Setup Guide

## Overview

로컬 환경에서 테이블오더 서비스를 실행하는 가이드입니다. AWS 배포 대비 **훨씬 빠르고 간단**합니다!

**소요 시간**: 30-45분 (AWS 배포 4.5-6시간 대비 **90% 단축**)  
**비용**: $0 (무료!)

---

## Time Comparison

| 환경 | 소요 시간 | 비용 | 복잡도 |
|------|----------|------|--------|
| **로컬 개발** | **30-45분** | **$0** | **낮음** |
| AWS 배포 | 4.5-6시간 | $56-67/월 | 높음 |

**권장**: 먼저 로컬에서 테스트 후, 필요 시 AWS 배포

---

## Prerequisites

### 필수 소프트웨어

1. **Python 3.9+**
   ```bash
   python --version
   # Python 3.9.0 이상
   ```

2. **Node.js 20+**
   ```bash
   node --version
   # v20.0.0 이상
   ```

3. **PostgreSQL 14+**
   - Windows: https://www.postgresql.org/download/windows/
   - 설치 시 비밀번호 설정 (예: `postgres`)

4. **Git** (이미 설치됨)

---

## Part 1: Backend Service Setup (15분)

### Step 1: PostgreSQL Database 생성

```bash
# PostgreSQL 접속 (비밀번호 입력)
psql -U postgres

# Database 생성
CREATE DATABASE tableorder;

# 확인 후 종료
\l
\q
```

### Step 2: Python 가상 환경 생성

```bash
# 프로젝트 루트로 이동
cd {workspace-root}

# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화 (Windows)
venv\Scripts\activate

# 의존성 설치
pip install -r config/requirements.txt
```

### Step 3: 환경 변수 설정

```bash
# .env 파일 생성 (프로젝트 루트)
cat > .env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tableorder
JWT_SECRET_KEY=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=16
SESSION_EXPIRE_HOURS=16
SESSION_LAST_ORDER_TIMEOUT_HOURS=2
ENVIRONMENT=development
FRONTEND_URL=http://localhost:5173,http://localhost:5174
LOG_LEVEL=DEBUG
LOG_FILE=logs/app.log
AWS_REGION=ap-northeast-2
S3_BUCKET_NAME=local-bucket
^Z
```

**중요**: `postgres:postgres` 부분을 실제 PostgreSQL 비밀번호로 변경하세요!

### Step 4: Database 스키마 생성

```bash
# Python 실행하여 스키마 생성
python -c "from src.database import engine, Base; from src.models import *; Base.metadata.create_all(bind=engine)"
```

### Step 5: Backend 서버 실행

```bash
# 로그 디렉토리 생성
mkdir logs

# FastAPI 서버 실행
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 출력:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process
```

### Step 6: Backend 확인

**새 터미널 열기**:
```bash
# Health Check
curl http://localhost:8000/health

# 예상 응답: {"status":"healthy"}

# API Docs 확인
# 브라우저에서: http://localhost:8000/docs
```

✅ **Backend 완료!** (약 15분)

---

## Part 2: Customer Frontend Setup (10분)

### Step 1: 의존성 설치

```bash
# 새 터미널 열기
cd customer-frontend

# 의존성 설치
npm install
```

### Step 2: 환경 변수 확인

```bash
# .env.development 파일 확인
cat .env.development

# 내용:
# VITE_API_URL=http://localhost:8000
# VITE_ENV=development
```

### Step 3: Frontend 서버 실행

```bash
# Vite Dev Server 실행
npm run dev

# 출력:
# VITE v5.0.0  ready in 500 ms
# ➜  Local:   http://localhost:5173/
```

### Step 4: Customer Frontend 확인

**브라우저에서 접속**: http://localhost:5173

**테스트**:
- 로그인 페이지 로드 확인
- 테이블 로그인 (store_id: 1, table_number: 1, pin: 1234)
- 메뉴 조회 (아직 메뉴 없음)

✅ **Customer Frontend 완료!** (약 10분)

---

## Part 3: Admin Frontend Setup (10분)

### Step 1: Admin Frontend 구현 (필요 시)

**Admin Frontend는 핵심 파일만 생성되었으므로, 빠른 테스트를 위해 최소 구현**:

```bash
cd admin-frontend

# Customer Frontend에서 공통 파일 복사
mkdir -p src/components/shared
mkdir -p src/services
mkdir -p src/composables

# 공통 컴포넌트 복사
cp -r ../customer-frontend/src/components/shared/* src/components/shared/
cp ../customer-frontend/src/assets/main.css src/assets/
cp ../customer-frontend/tailwind.config.js .
cp ../customer-frontend/postcss.config.js .
cp ../customer-frontend/.eslintrc.js .
cp ../customer-frontend/.gitignore .

# API Service 복사 (Admin용으로 수정 필요)
cp ../customer-frontend/src/services/api.js src/services/

# Toast Store 복사
cp ../customer-frontend/src/stores/toast.js src/stores/
cp ../customer-frontend/src/composables/useToast.js src/composables/
```

### Step 2: 의존성 설치

```bash
# 의존성 설치
npm install
```

### Step 3: 환경 변수 설정

```bash
# .env.development 파일 확인/생성
cat > .env.development
VITE_API_URL=http://localhost:8000
VITE_ENV=development
^Z
```

### Step 4: Admin Frontend 서버 실행

```bash
# Vite Dev Server 실행 (포트 5174)
npm run dev

# 출력:
# VITE v5.0.0  ready in 500 ms
# ➜  Local:   http://localhost:5174/
```

### Step 5: Admin Frontend 확인

**브라우저에서 접속**: http://localhost:5174

**참고**: Admin Frontend는 핵심 파일만 있으므로, 완전한 기능을 위해서는 나머지 파일 구현 필요 (admin-frontend/README.md 참조)

✅ **Admin Frontend 완료!** (약 10분)

---

## Part 4: 통합 테스트 (5분)

### 전체 시스템 테스트

**실행 중인 서비스 확인**:
- ✅ Backend: http://localhost:8000
- ✅ Customer Frontend: http://localhost:5173
- ✅ Admin Frontend: http://localhost:5174

### 테스트 시나리오

#### 1. 관리자 로그인 및 메뉴 추가

**Backend API 직접 호출** (Postman 또는 curl):

```bash
# 1. 관리자 로그인
curl -X POST http://localhost:8000/api/auth/admin-login \
  -H "Content-Type: application/json" \
  -d "{\"store_id\":1,\"username\":\"admin\",\"password\":\"admin123\"}"

# 응답에서 token 복사

# 2. 메뉴 추가
curl -X POST http://localhost:8000/api/admin/menus \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d "{\"store_id\":1,\"name\":\"김치찌개\",\"price\":8000,\"category\":\"메인\",\"description\":\"맛있는 김치찌개\",\"is_available\":true}"
```

#### 2. 고객 주문 플로우

**Customer Frontend** (http://localhost:5173):
1. 테이블 로그인 (store_id: 1, table_number: 1, pin: 1234)
2. 메뉴 조회 (위에서 추가한 메뉴 확인)
3. 장바구니 추가
4. 주문 생성

#### 3. 관리자 주문 확인

**Admin Frontend** (http://localhost:5174):
1. 관리자 로그인 (store_id: 1, username: admin, password: admin123)
2. 주문 대시보드에서 주문 확인 (구현 완료 시)

✅ **통합 테스트 완료!** (약 5분)

---

## Troubleshooting

### Issue 1: PostgreSQL 연결 실패

**증상**: `psycopg2.OperationalError: could not connect to server`

**해결**:
1. PostgreSQL 서비스 실행 확인
   ```bash
   # Windows Services에서 "postgresql" 검색
   # 또는 pgAdmin 실행
   ```
2. .env 파일의 DATABASE_URL 확인
3. 비밀번호 확인

### Issue 2: 포트 충돌

**증상**: `Error: listen EADDRINUSE: address already in use :::8000`

**해결**:
```bash
# 포트 사용 중인 프로세스 확인
netstat -ano | findstr :8000

# 프로세스 종료
taskkill /PID {process-id} /F

# 또는 다른 포트 사용
uvicorn src.main:app --reload --port 8001
```

### Issue 3: npm install 실패

**증상**: `npm ERR! code ERESOLVE`

**해결**:
```bash
# 캐시 정리
npm cache clean --force

# 재설치
npm install --legacy-peer-deps
```

### Issue 4: CORS 에러

**증상**: `Access to XMLHttpRequest has been blocked by CORS policy`

**해결**:
1. Backend .env 파일의 FRONTEND_URL 확인
2. Backend 재시작
3. 브라우저 캐시 삭제 (Ctrl+Shift+Delete)

---

## Development Workflow

### 코드 변경 시

**Backend**:
- FastAPI는 `--reload` 옵션으로 자동 재시작
- 코드 저장 시 자동 반영

**Frontend**:
- Vite는 Hot Module Replacement (HMR) 지원
- 코드 저장 시 브라우저 자동 새로고침

### Database 스키마 변경 시

```bash
# 1. models.py 수정
# 2. Database 재생성
python -c "from src.database import engine, Base; from src.models import *; Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)"

# 또는 Alembic 마이그레이션 사용 (설정 필요)
```

---

## Quick Start Script

**전체 시스템 한 번에 실행** (Windows):

```batch
@echo off
echo Starting TableOrder Services...

REM Backend
start cmd /k "cd /d %~dp0 && venv\Scripts\activate && uvicorn src.main:app --reload --port 8000"

REM Customer Frontend
start cmd /k "cd /d %~dp0customer-frontend && npm run dev"

REM Admin Frontend
start cmd /k "cd /d %~dp0admin-frontend && npm run dev"

echo All services started!
echo Backend: http://localhost:8000
echo Customer: http://localhost:5173
echo Admin: http://localhost:5174
pause
```

**파일 저장**: `start-all.bat`

**실행**:
```bash
start-all.bat
```

---

## Local vs AWS Comparison

| 항목 | 로컬 개발 | AWS 배포 |
|------|----------|----------|
| **소요 시간** | 30-45분 | 4.5-6시간 |
| **비용** | $0 | $56-67/월 |
| **복잡도** | 낮음 | 높음 |
| **인터넷 필요** | 불필요 | 필수 |
| **확장성** | 제한적 | 무제한 |
| **접근성** | 로컬만 | 전 세계 |
| **데이터 보존** | 로컬 DB | 클라우드 DB |
| **모니터링** | 수동 | CloudWatch |
| **백업** | 수동 | 자동 |

**권장 사용 시나리오**:
- **로컬 개발**: 개발, 테스트, 데모, 학습
- **AWS 배포**: 프로덕션, 실제 서비스, 다중 사용자

---

## Next Steps

### 1. 로컬 개발 완료 후

- [ ] Admin Frontend 나머지 파일 구현 (2시간)
- [ ] Priority 1 테스트 구현 (2-3시간)
- [ ] 통합 테스트 실행 (1시간)
- [ ] 성능 테스트 (선택사항)

### 2. AWS 배포 준비 (필요 시)

- [ ] 로컬 테스트 완료 확인
- [ ] AWS 계정 생성
- [ ] 배포 가이드 참조 (`deployment-guide.md`)
- [ ] Backend 배포 (`backend-deployment.md`)
- [ ] Frontend 배포 (`frontend-deployment.md`)

### 3. 프로덕션 준비

- [ ] 환경 변수 보안 강화
- [ ] 테스트 커버리지 80% 달성
- [ ] 성능 최적화
- [ ] 보안 테스트
- [ ] 문서화 완료

---

## Summary

**로컬 개발 환경 설정**:
- ✅ 소요 시간: 30-45분 (AWS 대비 90% 단축)
- ✅ 비용: $0 (무료)
- ✅ 복잡도: 낮음
- ✅ 즉시 테스트 가능

**권장 워크플로우**:
1. 로컬에서 개발 및 테스트 (30-45분)
2. 기능 완성 및 테스트 (2-5시간)
3. AWS 배포 (필요 시, 4.5-6시간)

**결론**: 로컬 개발이 훨씬 빠르고 간단합니다! 먼저 로컬에서 테스트 후, 필요 시 AWS 배포를 권장합니다.

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
