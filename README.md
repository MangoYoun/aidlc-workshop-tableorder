# TableOrder Backend Service

테이블오더 서비스의 Backend API 서버입니다.

## 기술 스택

- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Testing**: pytest

## 프로젝트 구조

```
├── src/
│   ├── main.py              # FastAPI 애플리케이션 (모든 API 엔드포인트)
│   ├── models.py            # Database 모델 (8개 엔티티)
│   ├── services.py          # 비즈니스 로직 (Auth, Menu, Order, Session)
│   ├── utils.py             # 유틸리티 (Security, Session)
│   ├── database.py          # Database 설정
│   └── config.py            # 환경 설정
├── tests/
│   └── test_services.py     # 테스트 케이스
├── config/
│   ├── requirements.txt     # Python 의존성
│   └── .env.example         # 환경 변수 예시
└── aidlc-docs/              # 설계 문서
```

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r config/requirements.txt
```

### 2. 환경 변수 설정

```bash
cp config/.env.example .env
# .env 파일을 편집하여 DATABASE_URL 등 설정
```

### 3. Database 설정

PostgreSQL 데이터베이스를 생성하고 .env 파일에 연결 정보를 입력합니다:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/tableorder
```

### 4. 서버 실행

```bash
# 개발 모드
python -m src.main

# 또는 uvicorn 직접 실행
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

서버가 실행되면 다음 URL에서 확인할 수 있습니다:
- API 서버: http://localhost:8000
- API 문서 (Swagger): http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## API 엔드포인트

### 인증 (Authentication)

- `POST /api/auth/admin-login` - 관리자 로그인
- `POST /api/auth/table-login` - 테이블 로그인

### 메뉴 (Menu)

- `GET /api/menus?store_id={id}` - 메뉴 목록 조회
- `POST /api/admin/menus` - 메뉴 생성 (관리자)
- `PUT /api/admin/menus/{menu_id}` - 메뉴 수정 (관리자)
- `DELETE /api/admin/menus/{menu_id}` - 메뉴 삭제 (관리자)

### 주문 (Order)

- `POST /api/orders` - 주문 생성
- `GET /api/orders` - 주문 내역 조회 (현재 세션)
- `GET /api/admin/orders?store_id={id}` - 모든 주문 조회 (관리자)
- `PUT /api/admin/orders/{order_id}/status` - 주문 상태 변경 (관리자)

### 세션 (Session)

- `POST /api/admin/sessions/{session_id}/close` - 세션 종료 (관리자)

### 헬스 체크

- `GET /health` - 서버 상태 확인

## 테스트 실행

```bash
pytest tests/ -v
```

## 주요 기능

### 보안 (Story 3.2)

- ✅ JWT 기반 인증 (16시간 만료)
- ✅ bcrypt 비밀번호 해싱
- ✅ 로그인 시도 제한 (5회 실패 시 15분 잠금)
- ✅ 관리자 권한 검증 (Middleware)
- ✅ SQL Injection 방지 (ORM 사용)

### 성능 (Story 3.1)

- ✅ Database 연결 풀링 (pool_size=5, max_overflow=10)
- ✅ API 응답 시간 모니터링 (Timing Middleware)
- ✅ 500ms 초과 시 WARNING 로그
- ✅ Database 인덱스 최적화

### 가용성 (Story 3.3)

- ✅ 구조화된 로깅 (Python logging)
- ✅ 사용자 친화적 에러 메시지
- ✅ 세션 만료 처리 (16시간 OR 마지막 주문 후 2시간)
- ✅ Health Check 엔드포인트

## 환경 변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| DATABASE_URL | PostgreSQL 연결 URL | - |
| JWT_SECRET_KEY | JWT 서명 키 | - |
| JWT_EXPIRE_HOURS | JWT 만료 시간 (시간) | 16 |
| SESSION_EXPIRE_HOURS | 세션 만료 시간 (시간) | 16 |
| SESSION_LAST_ORDER_TIMEOUT_HOURS | 마지막 주문 후 타임아웃 (시간) | 2 |
| ENVIRONMENT | 환경 (development/production) | development |
| FRONTEND_URL | Frontend URL (CORS) | http://localhost:3000 |
| LOG_LEVEL | 로그 레벨 | INFO |

## 개발 문서

상세한 설계 문서는 `aidlc-docs/` 디렉토리에서 확인할 수 있습니다:

- **Requirements**: `aidlc-docs/inception/requirements/requirements.md`
- **User Stories**: `aidlc-docs/inception/user-stories/stories.md`
- **Functional Design**: `aidlc-docs/construction/backend-service/functional-design/`
- **NFR Design**: `aidlc-docs/construction/backend-service/nfr-design/`
- **Infrastructure Design**: `aidlc-docs/construction/backend-service/infrastructure-design/`
- **TDD Plans**: `aidlc-docs/construction/plans/backend-service-*.md`

## 라이선스

MIT License
