# NFR Design Patterns - Backend Service

## Overview

Backend Service의 비기능 요구사항(NFR)을 충족하기 위한 설계 패턴과 구현 전략을 정의합니다.

---

## 1. Performance Patterns (성능 패턴)

### 1.1 Database Connection Pooling

**목적**: 데이터베이스 연결 재사용으로 성능 향상

**패턴**: Connection Pool Pattern

**구현 전략**:
- SQLAlchemy의 기본 연결 풀 사용
- 설정:
  - `pool_size=5`: 기본 연결 5개 유지
  - `max_overflow=10`: 추가로 10개까지 연결 생성 가능
  - 총 최대 15개 연결 지원

**코드 예시**:
```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True  # 연결 유효성 체크
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

**이점**:
- 연결 생성/종료 오버헤드 감소
- 동시 사용자 10-50명 지원 가능
- 연결 재사용으로 응답 시간 단축

---

### 1.2 Database Indexing Strategy

**목적**: 쿼리 성능 최적화

**패턴**: Index Optimization Pattern

**구현 전략**:
- 복합 인덱스 적극 활용
- 자주 조회되는 필드 조합에 인덱스 생성

**인덱스 목록**:

**AdminUser 테이블**:
- `(store_id, username)` - 로그인 조회 최적화

**TableAuth 테이블**:
- `(store_id, table_number)` - 테이블 로그인 조회 최적화

**TableSession 테이블**:
- `session_token` - 세션 조회 최적화
- `(table_auth_id, is_active)` - 활성 세션 조회 최적화

**Category 테이블**:
- `(store_id, display_order)` - 카테고리 목록 조회 최적화

**Menu 테이블**:
- `(category_id, display_order)` - 카테고리별 메뉴 조회 최적화
- `(store_id, is_available)` - 판매 가능 메뉴 조회 최적화

**Order 테이블**:
- `order_number` - 주문 번호 조회 최적화
- `(table_session_id, created_at)` - 세션별 주문 조회 최적화
- `(store_id, status, created_at)` - 매장별 상태별 주문 조회 최적화

**OrderItem 테이블**:
- `order_id` - 주문별 아이템 조회 최적화

**코드 예시**:
```python
# models.py
from sqlalchemy import Index

class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    username = Column(String(50))
    
    __table_args__ = (
        Index('idx_admin_user_store_username', 'store_id', 'username'),
    )
```

**이점**:
- 쿼리 응답 시간 대폭 감소
- 복합 인덱스로 다중 조건 쿼리 최적화
- API 응답 시간 500ms 이하 달성

---

### 1.3 API Response Time Monitoring

**목적**: API 성능 모니터링 및 병목 지점 식별

**패턴**: Monitoring Middleware Pattern

**구현 전략**:
- FastAPI Middleware에서 요청/응답 시간 측정
- 로그에 응답 시간 기록
- 500ms 초과 시 WARNING 로그

**코드 예시**:
```python
# middleware/timing.py
import time
import logging
from fastapi import Request

logger = logging.getLogger(__name__)

async def timing_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # 로깅
    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s"
    )
    
    # 500ms 초과 시 경고
    if process_time > 0.5:
        logger.warning(
            f"Slow API: {request.method} {request.url.path} took {process_time:.3f}s"
        )
    
    return response
```

**이점**:
- 실시간 성능 모니터링
- 느린 API 자동 감지
- 성능 개선 포인트 식별 용이

---

### 1.4 Query Optimization

**목적**: N+1 쿼리 문제 방지 및 쿼리 최적화

**패턴**: Eager Loading Pattern

**구현 전략**:
- SQLAlchemy의 `joinedload` 또는 `selectinload` 사용
- 관련 데이터를 한 번에 로드

**코드 예시**:
```python
# repositories/order_repository.py
from sqlalchemy.orm import joinedload

def get_order_with_items(order_id: int):
    return db.query(Order)\
        .options(joinedload(Order.order_items))\
        .filter(Order.id == order_id)\
        .first()
```

**이점**:
- N+1 쿼리 문제 방지
- 데이터베이스 왕복 횟수 감소
- 응답 시간 단축

---

## 2. Security Patterns (보안 패턴)

### 2.1 Password Hashing

**목적**: 비밀번호 안전한 저장

**패턴**: Cryptographic Hashing Pattern

**구현 전략**:
- Passlib 라이브러리 사용
- bcrypt 알고리즘 사용
- 최소 8자 이상 비밀번호 요구

**코드 예시**:
```python
# utils/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """비밀번호 해싱"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호 검증"""
    return pwd_context.verify(plain_password, hashed_password)
```

**이점**:
- 비밀번호 평문 저장 방지
- bcrypt의 강력한 보안
- 레인보우 테이블 공격 방어

---

### 2.2 JWT Authentication

**목적**: 상태 비저장(stateless) 인증

**패턴**: Token-Based Authentication Pattern

**구현 전략**:
- JWT 토큰 발급 및 검증
- 16시간 만료 시간
- user_type (table/admin) 구분

**코드 예시**:
```python
# utils/jwt.py
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "your-secret-key"  # .env에서 로드
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 16

def create_access_token(data: dict) -> str:
    """JWT 토큰 생성"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    """JWT 토큰 검증"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

**이점**:
- 서버 측 세션 저장 불필요
- 확장 가능한 인증 메커니즘
- 토큰에 사용자 정보 포함 가능

---

### 2.3 Login Attempt Limiting

**목적**: 브루트포스 공격 방지

**패턴**: Rate Limiting Pattern (User-based)

**구현 전략**:
- Database에 실패 횟수 저장
- 5회 실패 시 15분 잠금
- 성공 시 카운터 초기화

**코드 예시**:
```python
# services/auth_service.py
from datetime import datetime, timedelta

def check_login_attempts(user):
    """로그인 시도 제한 확인"""
    if user.locked_until and user.locked_until > datetime.utcnow():
        remaining = (user.locked_until - datetime.utcnow()).seconds // 60
        raise Exception(f"계정이 잠겼습니다. {remaining}분 후 다시 시도해주세요")

def handle_failed_login(user):
    """로그인 실패 처리"""
    user.failed_login_attempts += 1
    
    if user.failed_login_attempts >= 5:
        user.locked_until = datetime.utcnow() + timedelta(minutes=15)
    
    db.commit()

def handle_successful_login(user):
    """로그인 성공 처리"""
    user.failed_login_attempts = 0
    user.locked_until = None
    db.commit()
```

**이점**:
- 브루트포스 공격 방어
- 계정 보안 강화
- 자동 잠금 해제

---

### 2.4 Path-Based Authorization

**목적**: 관리자 전용 API 보호

**패턴**: Middleware Authorization Pattern

**구현 전략**:
- `/api/admin/*` 경로는 관리자만 접근
- JWT의 user_type 확인
- 권한 없으면 403 Forbidden

**코드 예시**:
```python
# middleware/auth.py
from fastapi import Request, HTTPException

async def auth_middleware(request: Request, call_next):
    # /api/admin/* 경로 체크
    if request.url.path.startswith("/api/admin/"):
        token = request.headers.get("Authorization")
        
        if not token:
            raise HTTPException(status_code=401, detail="인증이 필요합니다")
        
        payload = verify_token(token.replace("Bearer ", ""))
        
        if not payload or payload.get("user_type") != "admin":
            raise HTTPException(status_code=403, detail="관리자 권한이 필요합니다")
    
    response = await call_next(request)
    return response
```

**이점**:
- 간단한 권한 제어
- 경로 기반으로 명확한 구분
- 중앙 집중식 권한 관리

---

### 2.5 SQL Injection Prevention

**목적**: SQL Injection 공격 방지

**패턴**: ORM Pattern

**구현 전략**:
- SQLAlchemy ORM 사용
- 파라미터화된 쿼리 자동 생성
- 직접 SQL 문자열 조합 금지

**코드 예시**:
```python
# ❌ 잘못된 방법 (SQL Injection 취약)
def get_user_bad(username: str):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)

# ✅ 올바른 방법 (ORM 사용)
def get_user_good(username: str):
    return db.query(User).filter(User.username == username).first()
```

**이점**:
- SQL Injection 자동 방어
- 안전한 쿼리 생성
- 코드 가독성 향상

---

## 3. Availability Patterns (가용성 패턴)

### 3.1 Structured Logging

**목적**: 체계적인 로그 관리

**패턴**: Structured Logging Pattern

**구현 전략**:
- Python logging 모듈 사용
- 로그 레벨: DEBUG, INFO, WARNING, ERROR
- 로그 포맷: 타임스탬프, 레벨, 요청 ID, 사용자 ID, 메시지

**코드 예시**:
```python
# config/logging.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 사용 예시
logger.info(f"Order created: order_id={order.id}, table_id={table.id}")
logger.error(f"Database error: {str(e)}", exc_info=True)
```

**이점**:
- 문제 추적 용이
- 로그 분석 가능
- 디버깅 효율성 향상

---

### 3.2 Log Rotation

**목적**: 로그 파일 크기 관리

**패턴**: Log Rotation Pattern

**구현 전략**:
- RotatingFileHandler 사용
- 파일 크기 10MB 초과 시 로테이션
- 최대 5개 백업 파일 유지

**코드 예시**:
```python
# config/logging.py
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)

logger.addHandler(handler)
```

**이점**:
- 디스크 공간 절약
- 로그 파일 관리 자동화
- 오래된 로그 자동 삭제

---

### 3.3 User-Friendly Error Messages

**목적**: 사용자에게 명확한 에러 메시지 제공

**패턴**: Error Translation Pattern

**구현 전략**:
- 내부 에러를 사용자 친화적 메시지로 변환
- 에러 코드와 메시지 분리
- 한글 에러 메시지

**코드 예시**:
```python
# utils/errors.py
class AppException(Exception):
    def __init__(self, code: str, message: str, details: dict = None):
        self.code = code
        self.message = message
        self.details = details or {}

# 사용 예시
raise AppException(
    code="VALIDATION_ERROR",
    message="가격은 양수여야 합니다",
    details={"field": "price", "value": -1000}
)

# Exception Handler
@app.exception_handler(AppException)
async def app_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )
```

**이점**:
- 사용자 경험 향상
- 에러 원인 명확히 전달
- 디버깅 정보 제공

---

### 3.4 Health Check Endpoint

**목적**: 서버 상태 확인

**패턴**: Health Check Pattern

**구현 전략**:
- `/health` 엔드포인트 제공
- 200 OK 응답으로 서버 정상 확인

**코드 예시**:
```python
# main.py
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow()}
```

**이점**:
- 서버 상태 모니터링
- 로드 밸런서 헬스 체크
- 배포 검증 용이

---

## 4. Resilience Patterns (복원력 패턴)

### 4.1 Transaction Management

**목적**: 데이터 일관성 보장

**패턴**: Unit of Work Pattern

**구현 전략**:
- Service 레벨에서 트랜잭션 관리
- 에러 발생 시 명시적 롤백
- 트랜잭션 실패 로깅

**코드 예시**:
```python
# services/order_service.py
def create_order(session_id: int, items: list):
    try:
        # 트랜잭션 시작
        order = Order(session_id=session_id, status="pending")
        db.add(order)
        
        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                menu_id=item.menu_id,
                quantity=item.quantity
            )
            db.add(order_item)
        
        # 커밋
        db.commit()
        return order
        
    except Exception as e:
        # 롤백
        db.rollback()
        logger.error(f"Order creation failed: {str(e)}", exc_info=True)
        raise
```

**이점**:
- 데이터 일관성 보장
- 부분 실패 방지
- 에러 추적 용이

---

### 4.2 CORS Configuration

**목적**: Cross-Origin 요청 허용

**패턴**: CORS Middleware Pattern

**구현 전략**:
- 개발 환경: 모든 Origin 허용
- 프로덕션: Frontend URL만 허용

**코드 예시**:
```python
# main.py
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# 환경에 따라 CORS 설정
if os.getenv("ENVIRONMENT") == "production":
    origins = ["https://your-frontend-domain.com"]
else:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**이점**:
- Frontend-Backend 통신 허용
- 환경별 보안 설정
- 개발 편의성 제공

---

## Pattern Summary

| 카테고리 | 패턴 | 목적 |
|----------|------|------|
| Performance | Connection Pooling | DB 연결 재사용 |
| Performance | Database Indexing | 쿼리 최적화 |
| Performance | Response Time Monitoring | 성능 모니터링 |
| Performance | Query Optimization | N+1 쿼리 방지 |
| Security | Password Hashing | 비밀번호 보호 |
| Security | JWT Authentication | 상태 비저장 인증 |
| Security | Login Attempt Limiting | 브루트포스 방어 |
| Security | Path-Based Authorization | 권한 제어 |
| Security | SQL Injection Prevention | 공격 방어 |
| Availability | Structured Logging | 로그 관리 |
| Availability | Log Rotation | 파일 크기 관리 |
| Availability | User-Friendly Errors | 사용자 경험 |
| Availability | Health Check | 상태 확인 |
| Resilience | Transaction Management | 데이터 일관성 |
| Resilience | CORS Configuration | Cross-Origin 허용 |

**Total**: 15개 설계 패턴

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
