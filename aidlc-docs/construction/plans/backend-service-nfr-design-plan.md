# Backend Service - NFR Design Plan

## Plan Overview

이 계획은 Backend Service Unit의 비기능 요구사항(NFR)을 설계 패턴과 논리적 컴포넌트로 구체화하기 위한 계획입니다.

**Unit**: Backend Service  
**NFR Stories**: Story 3.1 (성능), Story 3.2 (보안), Story 3.3 (가용성)

---

## Execution Checklist

### Phase 1: Performance Design
- [x] API 응답 시간 최적화 패턴 정의
- [x] 데이터베이스 쿼리 최적화 전략
- [x] 캐싱 전략 (선택사항)
- [x] 동시 사용자 처리 패턴

### Phase 2: Security Design
- [x] 인증 및 권한 패턴
- [x] 비밀번호 해싱 및 저장
- [x] 로그인 시도 제한 메커니즘
- [x] SQL Injection 방지 전략

### Phase 3: Availability Design
- [x] 에러 로깅 패턴
- [x] 에러 처리 및 복구 전략
- [x] 세션 만료 알림 메커니즘
- [x] 네트워크 에러 재시도 패턴

### Phase 4: Logical Components
- [x] 인프라 컴포넌트 식별 (캐시, 큐 등)
- [x] 외부 서비스 통합 (없음)
- [x] 모니터링 및 로깅 컴포넌트

### Phase 5: Documentation
- [x] nfr-design-patterns.md 생성
- [x] logical-components.md 생성

---

## NFR Design Questions

다음 질문들에 답변하여 Backend Service의 NFR 설계 방향을 결정해주세요.

### Question 1: 데이터베이스 연결 풀링
데이터베이스 연결을 어떻게 관리하시겠습니까?

**Context**: 동시 사용자 10-50명을 지원해야 하며, API 응답 시간은 500ms 이하여야 합니다.

A) SQLAlchemy 기본 연결 풀 사용 (pool_size=5, max_overflow=10)
B) 커스텀 연결 풀 설정 (pool_size=20, max_overflow=30)
C) 연결 풀 없이 매 요청마다 새 연결 생성
D) 비동기 연결 풀 사용 (asyncpg)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: SQLAlchemy의 기본 연결 풀 설정이 중소규모 애플리케이션에 적합합니다. pool_size=5는 동시 연결 5개, max_overflow=10은 추가로 10개까지 연결 가능하여 총 15개 연결을 지원합니다. 동시 사용자 10-50명에 충분합니다.

---

### Question 2: API 응답 시간 모니터링
API 응답 시간을 어떻게 모니터링하시겠습니까?

**Context**: API 응답 시간이 500ms 이하여야 합니다.

A) Middleware에서 요청/응답 시간 측정 및 로깅
B) APM 도구 사용 (New Relic, Datadog 등)
C) 커스텀 메트릭 수집 및 저장
D) 모니터링 없음 (수동 테스트만)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: Middleware에서 요청/응답 시간을 측정하고 로깅하는 것이 가장 간단합니다. 초보자에게 적합하며, 추가 비용이 들지 않습니다. APM 도구는 나중에 필요하면 추가할 수 있습니다.

---

### Question 3: 데이터베이스 인덱스 전략
데이터베이스 인덱스를 어떻게 관리하시겠습니까?

**Context**: 쿼리 최적화를 위해 인덱스가 필요합니다.

A) 자주 조회되는 필드에만 인덱스 생성 (선택적)
B) 모든 FK에 자동 인덱스 생성
C) 복합 인덱스 적극 활용 (store_id + 다른 필드)
D) 인덱스 없이 시작 후 성능 문제 발생 시 추가
E) Other (please describe after [Answer]: tag below)

[Answer]: C

**이유**: 복합 인덱스를 적극 활용하면 쿼리 성능이 크게 향상됩니다. 예: `(store_id, username)`, `(store_id, table_number)`, `(category_id, display_order)` 등. 매장별 조회가 많으므로 store_id를 포함한 복합 인덱스가 효과적입니다.

---

### Question 4: 캐싱 전략
캐싱을 사용하시겠습니까?

**Context**: 메뉴 데이터는 자주 조회되지만 변경은 드뭅니다.

A) 캐싱 없음 (Database 직접 조회)
B) In-memory 캐싱 (Python dict 또는 lru_cache)
C) Redis 캐싱
D) Database 쿼리 결과 캐싱 (SQLAlchemy query cache)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: 초기에는 캐싱 없이 시작하는 것이 간단합니다. 동시 사용자 10-50명 규모에서는 Database 직접 조회로도 충분합니다. 성능 문제가 발생하면 나중에 캐싱을 추가할 수 있습니다.

---

### Question 5: Rate Limiting (요청 제한)
API 요청 제한을 구현하시겠습니까?

**Context**: DDoS 공격이나 과도한 요청을 방지해야 합니다.

A) Rate Limiting 없음
B) IP 기반 Rate Limiting (예: 분당 100 요청)
C) 사용자 기반 Rate Limiting (JWT 토큰 기반)
D) Nginx/API Gateway에서 Rate Limiting
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: 초기에는 Rate Limiting 없이 시작하는 것이 간단합니다. 중소규모 매장 3-10개 환경에서는 과도한 요청이 발생할 가능성이 낮습니다. 필요하면 나중에 추가할 수 있습니다.

---

### Question 6: 로그 로테이션
로그 파일을 어떻게 관리하시겠습니까?

**Context**: 로그 파일이 계속 커지면 디스크 공간 문제가 발생할 수 있습니다.

A) 로그 로테이션 없음 (수동 관리)
B) Python logging의 RotatingFileHandler 사용 (크기 기반)
C) TimedRotatingFileHandler 사용 (일별 로테이션)
D) 외부 로그 관리 도구 (Logrotate)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

**이유**: RotatingFileHandler를 사용하면 로그 파일 크기가 일정 크기(예: 10MB)를 초과하면 자동으로 새 파일로 로테이션됩니다. 간단하고 효과적입니다.

---

### Question 7: 에러 알림
심각한 에러 발생 시 알림을 보내시겠습니까?

**Context**: 서버 오류 발생 시 관리자에게 즉시 알려야 할 수 있습니다.

A) 알림 없음 (로그 파일만)
B) 이메일 알림
C) Slack/Discord 알림
D) SMS 알림
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: 초기에는 로그 파일만으로 충분합니다. 알림 시스템은 추가 복잡도를 증가시키며, 초보자에게는 과도합니다. 필요하면 나중에 추가할 수 있습니다.

---

### Question 8: Health Check 엔드포인트
서버 상태 확인 엔드포인트를 만드시겠습니까?

**Context**: 서버가 정상 동작하는지 확인하기 위한 엔드포인트입니다.

A) Health Check 없음
B) 간단한 Health Check (`/health` → 200 OK)
C) 상세 Health Check (Database 연결, 디스크 공간 등 확인)
D) Readiness + Liveness Probe (Kubernetes용)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

**이유**: 간단한 Health Check 엔드포인트를 만들면 서버가 실행 중인지 확인할 수 있습니다. `/health` 엔드포인트가 200 OK를 반환하면 서버가 정상입니다. 간단하고 유용합니다.

---

### Question 9: CORS (Cross-Origin Resource Sharing)
CORS를 어떻게 설정하시겠습니까?

**Context**: Frontend와 Backend가 다른 포트에서 실행되므로 CORS 설정이 필요합니다.

A) 모든 Origin 허용 (`*`)
B) 특정 Origin만 허용 (Frontend URL)
C) 개발 환경에서만 모든 Origin 허용, 프로덕션에서는 제한
D) CORS 설정 없음
E) Other (please describe after [Answer]: tag below)

[Answer]: C

**이유**: 개발 환경에서는 편의를 위해 모든 Origin을 허용하고, 프로덕션에서는 보안을 위해 Frontend URL만 허용하는 것이 좋습니다. FastAPI의 CORSMiddleware를 사용하면 쉽게 설정할 수 있습니다.

---

### Question 10: 환경 변수 관리
환경 변수를 어떻게 관리하시겠습니까?

**Context**: Database URL, JWT Secret 등 민감한 정보를 관리해야 합니다.

A) .env 파일 사용 (python-dotenv)
B) 환경 변수 직접 설정 (export)
C) AWS Secrets Manager
D) 코드에 하드코딩 (절대 안 됨!)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: .env 파일을 사용하면 환경 변수를 쉽게 관리할 수 있습니다. python-dotenv 라이브러리로 .env 파일을 로드하면 됩니다. 간단하고 초보자에게 적합합니다. AWS Secrets Manager는 나중에 프로덕션 배포 시 고려할 수 있습니다.

---

## Instructions

모든 질문에 초보자 친화적인 답변이 이미 채워져 있습니다. 검토 후 승인해주시면 NFR Design 아티팩트 생성을 시작합니다.

---

**검토 후 승인해주세요.**
