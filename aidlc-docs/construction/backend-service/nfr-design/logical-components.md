# Logical Components - Backend Service

## Overview

Backend Service의 NFR 요구사항을 지원하기 위한 논리적 컴포넌트와 인프라 요소를 정의합니다.

---

## 1. Core Infrastructure Components

### 1.1 Database Component

**목적**: 데이터 영속성 및 트랜잭션 관리

**기술**: PostgreSQL

**구성 요소**:
- **Connection Pool**: SQLAlchemy 연결 풀 (pool_size=5, max_overflow=10)
- **Database Schema**: 8개 테이블 (Store, AdminUser, TableAuth, TableSession, Category, Menu, Order, OrderItem)
- **Indexes**: 복합 인덱스 (store_id 기반)
- **Transactions**: Service 레벨 트랜잭션 관리

**연결 정보**:
```python
DATABASE_URL = "postgresql://{user}:{password}@{host}:{port}/{database}"
```

**책임**:
- 데이터 저장 및 조회
- 트랜잭션 관리
- 데이터 무결성 보장
- 쿼리 최적화 (인덱스 활용)

---

### 1.2 Logging Component

**목적**: 애플리케이션 로그 수집 및 관리

**기술**: Python logging 모듈

**구성 요소**:
- **Logger**: 애플리케이션 로거
- **Handlers**: 
  - FileHandler (파일 저장)
  - StreamHandler (콘솔 출력)
  - RotatingFileHandler (로그 로테이션)
- **Formatters**: 타임스탬프, 레벨, 메시지 포맷

**로그 레벨**:
- DEBUG: 디버깅 정보
- INFO: 일반 정보 (API 요청, 주문 생성 등)
- WARNING: 경고 (느린 API, 세션 만료 임박 등)
- ERROR: 에러 (Database 에러, 비즈니스 로직 에러 등)

**로그 파일 구조**:
```
logs/
├── app.log          # 현재 로그
├── app.log.1        # 백업 1
├── app.log.2        # 백업 2
├── app.log.3        # 백업 3
├── app.log.4        # 백업 4
└── app.log.5        # 백업 5
```

**로그 로테이션**:
- 파일 크기: 10MB 초과 시 로테이션
- 백업 개수: 최대 5개

**책임**:
- 애플리케이션 이벤트 로깅
- 에러 추적 및 디버깅
- 성능 모니터링 (API 응답 시간)
- 로그 파일 크기 관리

---

### 1.3 Environment Configuration Component

**목적**: 환경 변수 및 설정 관리

**기술**: python-dotenv

**구성 요소**:
- **.env 파일**: 환경 변수 저장
- **Config 클래스**: 설정 로드 및 검증

**환경 변수 목록**:
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/tableorder

# JWT
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=16

# Session
SESSION_EXPIRE_HOURS=16
SESSION_LAST_ORDER_TIMEOUT_HOURS=2

# CORS
ENVIRONMENT=development  # or production
FRONTEND_URL=http://localhost:3000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

**책임**:
- 환경 변수 로드
- 설정 검증
- 민감한 정보 보호 (.env 파일은 .gitignore에 추가)

---

## 2. Middleware Components

### 2.1 Timing Middleware

**목적**: API 응답 시간 측정 및 모니터링

**위치**: FastAPI Middleware

**기능**:
- 요청 시작 시간 기록
- 응답 완료 시간 계산
- 응답 헤더에 `X-Process-Time` 추가
- 500ms 초과 시 WARNING 로그

**책임**:
- 성능 모니터링
- 느린 API 감지
- 응답 시간 로깅

---

### 2.2 Authentication Middleware

**목적**: JWT 토큰 검증 및 권한 확인

**위치**: FastAPI Middleware

**기능**:
- `/api/admin/*` 경로 체크
- JWT 토큰 검증
- user_type 확인 (admin/table)
- 권한 없으면 403 Forbidden

**책임**:
- 인증 확인
- 권한 제어
- 관리자 전용 API 보호

---

### 2.3 CORS Middleware

**목적**: Cross-Origin 요청 허용

**위치**: FastAPI Middleware

**기능**:
- 개발 환경: 모든 Origin 허용
- 프로덕션: Frontend URL만 허용
- Credentials 허용
- 모든 HTTP 메서드 허용

**책임**:
- Frontend-Backend 통신 허용
- 환경별 보안 설정

---

## 3. Security Components

### 3.1 Password Hashing Component

**목적**: 비밀번호 안전한 저장

**기술**: Passlib (bcrypt)

**기능**:
- 비밀번호 해싱
- 비밀번호 검증
- bcrypt 알고리즘 사용

**책임**:
- 비밀번호 평문 저장 방지
- 레인보우 테이블 공격 방어

---

### 3.2 JWT Token Component

**목적**: 상태 비저장 인증

**기술**: python-jose

**기능**:
- JWT 토큰 생성
- JWT 토큰 검증
- 16시간 만료 시간
- user_type (table/admin) 포함

**토큰 페이로드**:
```json
{
  "user_id": 123,
  "user_type": "admin",
  "store_id": 1,
  "exp": 1234567890
}
```

**책임**:
- 토큰 발급
- 토큰 검증
- 만료 시간 관리

---

### 3.3 Login Attempt Limiter

**목적**: 브루트포스 공격 방지

**위치**: Service Layer

**기능**:
- Database에 실패 횟수 저장
- 5회 실패 시 15분 잠금
- 성공 시 카운터 초기화

**Database 필드**:
- `failed_login_attempts`: 실패 횟수
- `locked_until`: 잠금 해제 시간

**책임**:
- 로그인 시도 제한
- 계정 잠금 관리
- 자동 잠금 해제

---

## 4. Monitoring Components

### 4.1 Health Check Endpoint

**목적**: 서버 상태 확인

**엔드포인트**: `GET /health`

**응답**:
```json
{
  "status": "ok",
  "timestamp": "2026-02-09T12:00:00Z"
}
```

**책임**:
- 서버 정상 동작 확인
- 로드 밸런서 헬스 체크
- 배포 검증

---

### 4.2 API Response Time Logger

**목적**: API 성능 추적

**위치**: Timing Middleware

**기능**:
- 모든 API 요청/응답 시간 로깅
- 500ms 초과 시 경고
- 응답 헤더에 시간 포함

**로그 포맷**:
```
[2026-02-09 12:00:00] [INFO] GET /api/menus - 200 - 0.123s
[2026-02-09 12:00:01] [WARNING] Slow API: POST /api/orders took 0.678s
```

**책임**:
- 성능 모니터링
- 병목 지점 식별
- 성능 개선 포인트 제공

---

## 5. External Service Integration

**현재 상태**: 외부 서비스 통합 없음

Backend Service는 현재 외부 서비스와 통합하지 않습니다. 모든 기능은 내부적으로 구현됩니다.

**향후 확장 가능성**:
- 결제 게이트웨이 (PG사 연동)
- SMS 알림 서비스
- 이메일 서비스
- 푸시 알림 서비스

---

## 6. Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Middleware Layer                         │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │  │
│  │  │  CORS    │  │  Timing  │  │  Authentication  │  │  │
│  │  └──────────┘  └──────────┘  └──────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ↓                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Controller Layer                         │  │
│  │  (API Endpoints)                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ↓                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Service Layer                            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │  │
│  │  │  Auth    │  │  Order   │  │  Menu            │  │  │
│  │  │  Service │  │  Service │  │  Service         │  │  │
│  │  └──────────┘  └──────────┘  └──────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ↓                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Repository Layer                         │  │
│  │  (Database Access)                                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ↓                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │  PostgreSQL  │  │  Logging     │  │  Environment     │ │
│  │  Database    │  │  System      │  │  Config          │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. Component Dependencies

| Component | Depends On | Used By |
|-----------|------------|---------|
| Database | Environment Config | Repository Layer |
| Logging | Environment Config | All Layers |
| Environment Config | .env file | All Components |
| Timing Middleware | Logging | FastAPI App |
| Auth Middleware | JWT Token, Logging | FastAPI App |
| CORS Middleware | Environment Config | FastAPI App |
| Password Hashing | - | Auth Service |
| JWT Token | Environment Config | Auth Service, Auth Middleware |
| Login Attempt Limiter | Database | Auth Service |
| Health Check | - | FastAPI App |
| API Response Logger | Logging | Timing Middleware |

---

## 8. Deployment Considerations

### 8.1 Environment-Specific Configuration

**Development**:
- CORS: 모든 Origin 허용
- LOG_LEVEL: DEBUG
- Database: 로컬 PostgreSQL

**Production**:
- CORS: Frontend URL만 허용
- LOG_LEVEL: INFO
- Database: AWS RDS PostgreSQL
- JWT_SECRET_KEY: 강력한 랜덤 키 사용

### 8.2 Required Infrastructure

**최소 요구사항**:
- PostgreSQL 12 이상
- Python 3.9 이상
- 디스크 공간: 최소 1GB (로그 파일 포함)

**권장 사양**:
- CPU: 2 cores
- RAM: 2GB
- 네트워크: 100Mbps

---

## Component Summary

| 카테고리 | 컴포넌트 | 기술 |
|----------|----------|------|
| Infrastructure | Database | PostgreSQL + SQLAlchemy |
| Infrastructure | Logging | Python logging |
| Infrastructure | Environment Config | python-dotenv |
| Middleware | Timing | FastAPI Middleware |
| Middleware | Authentication | FastAPI Middleware |
| Middleware | CORS | FastAPI CORSMiddleware |
| Security | Password Hashing | Passlib (bcrypt) |
| Security | JWT Token | python-jose |
| Security | Login Attempt Limiter | Database + Service Logic |
| Monitoring | Health Check | FastAPI Endpoint |
| Monitoring | API Response Logger | Timing Middleware |

**Total**: 11개 논리적 컴포넌트

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
