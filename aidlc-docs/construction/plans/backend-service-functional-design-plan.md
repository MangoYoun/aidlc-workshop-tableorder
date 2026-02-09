# Backend Service - Functional Design Plan

## Plan Overview

이 계획은 Backend Service Unit의 상세 비즈니스 로직 설계를 위한 계획입니다.

**Unit**: Backend Service  
**Assigned Stories**: Story 3.1 (성능), Story 3.2 (보안), Story 3.3 (가용성)  
**Focus**: RESTful API, 비즈니스 로직, 데이터베이스, 인증, 실시간 통신

---

## Execution Checklist

### Phase 1: Business Logic Analysis
- [x] 핵심 비즈니스 엔티티 식별
- [x] 비즈니스 워크플로우 정의
- [x] 데이터 변환 로직 설계

### Phase 2: Domain Model Design
- [x] 도메인 엔티티 정의 (User, Table, Menu, Order 등)
- [x] 엔티티 간 관계 정의
- [x] 데이터 구조 및 속성 정의

### Phase 3: Business Rules Definition
- [x] 검증 규칙 정의
- [x] 비즈니스 제약사항 정의
- [x] 의사결정 로직 정의

### Phase 4: Data Flow Design
- [x] API 입력/출력 데이터 정의
- [x] 데이터 변환 프로세스 정의
- [x] 데이터 영속성 요구사항 정의

### Phase 5: Integration Points
- [x] Frontend와의 API 계약 정의
- [x] 외부 시스템 통합 포인트 식별 (없음)
- [x] 데이터 교환 형식 정의

### Phase 6: Error Handling Strategy
- [x] 에러 시나리오 식별
- [x] 검증 실패 처리 전략
- [x] 예외 처리 로직 정의

### Phase 7: Documentation
- [x] business-logic-model.md 생성
- [x] domain-entities.md 생성
- [x] business-rules.md 생성

---

## Functional Design Questions

다음 질문들에 답변하여 Backend Service의 상세 기능 설계 방향을 결정해주세요.

### Question 1: 테이블 세션 관리 전략
테이블 세션을 어떻게 관리하시겠습니까?

**Context**: 테이블 세션은 16시간 OR 마지막 주문 후 일정 시간 중 먼저 도달하는 조건으로 만료됩니다.

A) Database에 세션 테이블 생성 (session_id, table_id, created_at, last_order_at, expired_at)
B) JWT 토큰에 세션 정보 포함 (stateless)
C) Redis 같은 캐시에 세션 저장 (빠른 조회)
D) Database + In-memory 캐시 조합
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: 초보자에게 가장 간단하고 명확합니다. Database에 세션 정보를 저장하면 세션 상태를 쉽게 추적하고 관리할 수 있습니다. Redis는 추가 인프라가 필요하고, JWT만으로는 세션 만료 조건(마지막 주문 시간)을 추적하기 어렵습니다.

**Follow-up**: 세션 만료 체크는 어떻게 수행하시겠습니까?
- 매 API 요청마다 체크
- 백그라운드 작업으로 주기적 체크
- 둘 다 사용

[Answer]: 매 API 요청마다 체크

**이유**: 간단하고 즉각적입니다. Middleware에서 세션 유효성을 체크하면 만료된 세션을 즉시 감지할 수 있습니다. 백그라운드 작업은 추가 복잡도를 증가시킵니다. 

---

### Question 2: 주문 상태 관리
주문의 상태 전이를 어떻게 관리하시겠습니까?

**Context**: 주문 상태는 "대기중 → 준비중 → 완료" 순서로 변경됩니다.

A) 단순 문자열 상태 (status: "pending", "preparing", "completed")
B) Enum 타입 상태 + 상태 전이 검증 로직
C) State Machine 패턴 (상태 전이 규칙 명시적 정의)
D) 상태 + 타임스탬프 (status_history 테이블로 이력 관리)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

**이유**: Enum 타입으로 상태를 정의하면 오타를 방지하고 타입 안정성을 확보할 수 있습니다. 상태 전이 검증 로직을 추가하면 잘못된 상태 변경을 방지할 수 있습니다. State Machine은 과도하게 복잡하고, 이력 관리는 현재 요구사항에 없습니다.

**Follow-up**: 잘못된 상태 전이 시도 (예: 완료 → 대기중) 처리 방법은?
- 에러 반환 (400 Bad Request)
- 무시하고 현재 상태 유지
- 로그만 남기고 허용

[Answer]: 에러 반환 (400 Bad Request)

**이유**: 명확한 에러 메시지로 클라이언트에게 잘못된 요청임을 알려주는 것이 가장 좋습니다. 무시하거나 허용하면 데이터 무결성 문제가 발생할 수 있습니다. 

---

### Question 3: 주문 데이터 구조
주문 데이터를 어떻게 저장하시겠습니까?

**Context**: 주문은 여러 메뉴 아이템과 수량을 포함합니다.

A) Order 테이블 + OrderItem 테이블 (정규화)
   - Order: id, table_id, session_id, total_amount, status, created_at
   - OrderItem: id, order_id, menu_id, quantity, price
B) Order 테이블에 JSON 필드로 아이템 저장 (비정규화)
   - Order: id, table_id, items (JSON), total_amount, status
C) Order + OrderItem + OrderItemSnapshot (메뉴 변경 대비)
   - OrderItemSnapshot: menu_name, price 스냅샷 저장
D) Other (please describe after [Answer]: tag below)

[Answer]: C

**이유**: 주문 시점의 메뉴 정보(이름, 가격)를 스냅샷으로 저장하면 나중에 메뉴가 변경되어도 주문 내역을 정확히 유지할 수 있습니다. 정규화된 구조로 데이터 무결성을 보장하면서도, 스냅샷으로 이력 보존이 가능합니다.

**Follow-up**: 주문 생성 후 메뉴 가격이 변경되면 어떻게 처리하시겠습니까?
- 주문 시점의 가격 유지 (스냅샷)
- 현재 메뉴 가격 참조
- 가격 변경 불가 정책

[Answer]: 주문 시점의 가격 유지 (스냅샷)

**이유**: 주문 시점의 가격을 유지하는 것이 비즈니스 관점에서 올바릅니다. 고객이 주문할 때 본 가격과 실제 청구 가격이 달라지면 안 됩니다. 

---

### Question 4: 메뉴 카테고리 관리
메뉴 카테고리를 어떻게 관리하시겠습니까?

**Context**: 메뉴는 카테고리별로 분류됩니다 (예: 메인, 사이드, 음료).

A) 단순 문자열 필드 (category: "메인", "사이드", "음료")
B) Category 테이블 별도 생성 (id, name, display_order)
C) 계층적 카테고리 (parent_category_id 지원)
D) 태그 기반 (메뉴가 여러 카테고리에 속할 수 있음)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

**이유**: Category 테이블을 별도로 만들면 카테고리 관리가 용이하고, display_order로 순서 조정이 가능합니다. 단순 문자열은 오타 위험이 있고, 계층적 구조는 현재 요구사항에 과도합니다.

**Follow-up**: 카테고리 순서 조정이 필요한가요?
- 필요 (display_order 필드 추가)
- 불필요 (알파벳 순 정렬)

[Answer]: 필요 (display_order 필드 추가)

**이유**: 관리자가 카테고리 표시 순서를 자유롭게 조정할 수 있어야 합니다. 알파벳 순은 비즈니스 요구에 맞지 않을 수 있습니다. 

---

### Question 5: 실시간 주문 업데이트 (SSE)
SSE를 통한 실시간 업데이트를 어떻게 구현하시겠습니까?

**Context**: 관리자는 신규 주문을 실시간으로 받아야 합니다.

A) 모든 관리자에게 브로드캐스트 (매장 단위)
B) 특정 테이블 주문만 구독 가능
C) 매장별 + 테이블별 필터링 지원
D) 이벤트 큐 사용 (Redis Pub/Sub, RabbitMQ 등)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: 가장 간단한 구현입니다. 매장 단위로 모든 관리자에게 주문 이벤트를 브로드캐스트하면 됩니다. 현재 요구사항(중소규모 매장 3-10개)에서는 충분하며, 추가 인프라(Redis, RabbitMQ)가 필요 없습니다.

**Follow-up**: SSE 연결이 끊어졌을 때 처리 방법은?
- 클라이언트 자동 재연결 (서버는 신경 안 씀)
- 서버에서 연결 상태 추적 및 재전송
- 연결 끊김 시 폴링으로 fallback

[Answer]: 클라이언트 자동 재연결 (서버는 신경 안 씀)

**이유**: SSE는 클라이언트가 자동으로 재연결을 시도합니다. 서버는 단순히 이벤트를 브로드캐스트하기만 하면 되므로 구현이 간단합니다. 

---

### Question 6: 인증 및 권한 관리
테이블 로그인과 관리자 로그인을 어떻게 구분하시겠습니까?

**Context**: 테이블은 자동 로그인, 관리자는 수동 로그인입니다.

A) 단일 User 테이블 + role 필드 ("table", "admin")
B) 별도 테이블 (TableAuth, AdminUser)
C) JWT 토큰의 claims로 구분 (role, user_type)
D) 별도 인증 엔드포인트 + 별도 JWT secret
E) Other (please describe after [Answer]: tag below)

[Answer]: B

**이유**: 테이블과 관리자는 속성이 완전히 다르므로 별도 테이블로 관리하는 것이 명확합니다. TableAuth는 table_id, store_id, password를 가지고, AdminUser는 username, password, store_id를 가집니다. JWT claims에는 user_type을 포함하여 구분합니다.

**Follow-up**: 테이블과 관리자의 API 접근 권한을 어떻게 제어하시겠습니까?
- Middleware에서 role 체크
- Decorator로 각 엔드포인트에 권한 명시
- 경로 기반 권한 (/api/admin/* 는 관리자만)

[Answer]: 경로 기반 권한 (/api/admin/* 는 관리자만)

**이유**: 가장 간단하고 명확합니다. `/api/admin/*` 경로는 관리자만, 나머지는 테이블 사용자가 접근 가능하도록 Middleware에서 체크하면 됩니다. 

---

### Question 7: 비밀번호 저장 및 검증
비밀번호를 어떻게 저장하고 검증하시겠습니까?

**Context**: 관리자 비밀번호와 테이블 비밀번호 모두 bcrypt 해싱이 필요합니다.

A) bcrypt 라이브러리 직접 사용
B) Passlib 같은 고수준 라이브러리 사용
C) FastAPI의 security utilities 사용
D) 커스텀 해싱 유틸리티 작성
E) Other (please describe after [Answer]: tag below)

[Answer]: B

**이유**: Passlib은 Python에서 가장 널리 사용되는 비밀번호 해싱 라이브러리입니다. bcrypt를 포함한 여러 해싱 알고리즘을 지원하며, 사용하기 쉽고 안전합니다. FastAPI 공식 문서에서도 Passlib을 권장합니다.

**Follow-up**: 비밀번호 복잡도 요구사항이 있나요?
- 없음 (자유롭게 설정)
- 최소 길이만 (예: 8자 이상)
- 복잡도 규칙 (대소문자, 숫자, 특수문자)

[Answer]: 최소 길이만 (예: 8자 이상)

**이유**: 초보자에게 적합한 수준입니다. 최소 8자 이상으로 설정하면 기본적인 보안을 확보할 수 있습니다. 복잡도 규칙은 사용자 경험을 해칠 수 있습니다. 

---

### Question 8: 로그인 시도 제한
로그인 시도 제한을 어떻게 구현하시겠습니까?

**Context**: 보안을 위해 로그인 시도 횟수를 제한해야 합니다.

A) In-memory 카운터 (서버 재시작 시 초기화)
B) Database에 실패 횟수 저장
C) Redis 같은 캐시에 TTL과 함께 저장
D) IP 기반 제한 + 사용자 기반 제한
E) Other (please describe after [Answer]: tag below)

[Answer]: B

**이유**: Database에 실패 횟수를 저장하면 서버 재시작 후에도 제한이 유지됩니다. Redis는 추가 인프라가 필요하고, In-memory는 재시작 시 초기화되어 보안에 취약합니다.

**Follow-up**: 제한 정책은 어떻게 하시겠습니까?
- 5회 실패 시 15분 잠금
- 3회 실패 시 5분 잠금
- 10회 실패 시 1시간 잠금
- 기타 (명시해주세요)

[Answer]: 5회 실패 시 15분 잠금

**이유**: 일반적으로 널리 사용되는 정책입니다. 너무 엄격하지 않으면서도 브루트포스 공격을 효과적으로 방어할 수 있습니다. 

---

### Question 9: 에러 로깅 전략
에러를 어떻게 로깅하시겠습니까?

**Context**: 가용성 요구사항으로 파일 로깅이 필요합니다.

A) Python logging 모듈 + 파일 핸들러
B) 구조화된 로깅 (JSON 형식)
C) 로그 레벨별 파일 분리 (error.log, info.log)
D) 로그 로테이션 (일별, 크기별)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: Python 표준 logging 모듈이 가장 간단하고 충분합니다. 파일 핸들러를 추가하면 로그를 파일에 저장할 수 있습니다. 구조화된 로깅이나 파일 분리는 나중에 필요하면 추가할 수 있습니다.

**Follow-up**: 로그에 포함할 정보는?
- 타임스탬프, 레벨, 메시지만
- + 요청 ID, 사용자 ID
- + 스택 트레이스, 요청 파라미터
- + 성능 메트릭 (응답 시간)

[Answer]: + 요청 ID, 사용자 ID

**이유**: 타임스탬프, 레벨, 메시지는 기본이고, 요청 ID와 사용자 ID를 추가하면 문제 추적이 용이합니다. 스택 트레이스는 에러 발생 시 자동으로 포함되며, 성능 메트릭은 현재 요구사항에 과도합니다. 

---

### Question 10: 데이터베이스 트랜잭션 관리
트랜잭션을 어떻게 관리하시겠습니까?

**Context**: 주문 생성 시 Order + OrderItem 동시 생성이 필요합니다.

A) SQLAlchemy의 자동 트랜잭션 사용
B) 명시적 트랜잭션 관리 (session.begin())
C) Repository 레벨에서 트랜잭션 관리
D) Service 레벨에서 트랜잭션 관리
E) Other (please describe after [Answer]: tag below)

[Answer]: D

**이유**: Service 레벨에서 트랜잭션을 관리하는 것이 가장 적절합니다. 비즈니스 로직이 Service에 있으므로, 트랜잭션 경계도 Service에서 정의하는 것이 명확합니다. Repository는 단순히 데이터 접근만 담당합니다.

**Follow-up**: 트랜잭션 실패 시 롤백 전략은?
- 자동 롤백 (SQLAlchemy 기본)
- 명시적 롤백 + 에러 로깅
- 재시도 메커니즘 (최대 3회)

[Answer]: 명시적 롤백 + 에러 로깅

**이유**: 트랜잭션 실패 시 명시적으로 롤백하고 에러를 로깅하면 문제 추적이 용이합니다. 재시도 메커니즘은 일시적 네트워크 오류에는 유용하지만, 대부분의 에러는 재시도해도 실패하므로 현재는 불필요합니다. 

---

## Instructions

1. 위의 모든 질문에 [Answer]: 태그 뒤에 선택한 옵션의 문자(A, B, C 등)를 입력해주세요.
2. 제공된 옵션이 맞지 않으면 마지막 옵션을 선택하고 설명을 추가해주세요.
3. Follow-up 질문에도 답변해주세요.
4. 모든 질문에 답변하신 후 "완료" 또는 "done"이라고 말씀해주세요.
5. 답변 완료 후, 이 계획을 검토하고 승인해주시면 Functional Design 아티팩트 생성을 시작합니다.

---

**모든 질문에 답변하신 후 "완료" 또는 "done"이라고 말씀해주세요.**
