# Unit of Work - Story Mapping

## Story to Unit Assignment

이 문서는 12개의 User Stories를 3개의 Units of Work에 매핑합니다.

---

## Mapping Summary

| Epic | Story | Unit | Priority |
|------|-------|------|----------|
| Epic 1 | Story 1.1: 테이블 자동 로그인 | Customer Frontend | High |
| Epic 1 | Story 1.2: 메뉴 조회 및 탐색 | Customer Frontend | High |
| Epic 1 | Story 1.3: 장바구니 관리 | Customer Frontend | High |
| Epic 1 | Story 1.4: 주문 생성 | Customer Frontend | High |
| Epic 1 | Story 1.5: 주문 내역 조회 | Customer Frontend | High |
| Epic 2 | Story 2.1: 매장 인증 | Admin Frontend | High |
| Epic 2 | Story 2.2: 실시간 주문 모니터링 | Admin Frontend | High |
| Epic 2 | Story 2.3: 테이블 관리 | Admin Frontend | High |
| Epic 2 | Story 2.4: 메뉴 관리 | Admin Frontend | High |
| Epic 3 | Story 3.1: 성능 요구사항 | Backend Service | High |
| Epic 3 | Story 3.2: 보안 요구사항 | Backend Service | High |
| Epic 3 | Story 3.3: 가용성 요구사항 | Backend Service | High |

---

## Unit 1: Backend Service

### Assigned Stories (3 stories)

#### Story 3.1: 성능 요구사항
**Epic**: Epic 3 (비기능 요구사항)  
**Size**: M  
**Priority**: High

**Implementation Scope**:
- API 응답 시간 최적화 (500ms 이하)
- 데이터베이스 쿼리 최적화
- 인덱스 설정
- 캐싱 전략 (선택사항)
- 동시 사용자 10-50명 지원

**Acceptance Criteria**:
- [ ] API 응답 시간이 500ms 이하이다
- [ ] 페이지 로딩 시간이 2초 이내이다
- [ ] 실시간 주문 업데이트가 2초 이내에 표시된다
- [ ] 동시 사용자 10-50명을 지원한다
- [ ] 데이터베이스 쿼리가 최적화되어 있다

---

#### Story 3.2: 보안 요구사항
**Epic**: Epic 3 (비기능 요구사항)  
**Size**: M  
**Priority**: High

**Implementation Scope**:
- JWT 기반 인증 구현
- 비밀번호 bcrypt 해싱
- 로그인 시도 제한
- 권한 검증 middleware
- SQL Injection 방지 (ORM 사용)
- 환경변수 관리 (.env)

**Acceptance Criteria**:
- [ ] JWT 기반 인증이 구현되어 있다
- [ ] 비밀번호가 bcrypt로 해싱되어 저장된다
- [ ] 로그인 시도 제한이 구현되어 있다
- [ ] 관리자 전용 기능에 권한 검증이 있다
- [ ] SQL Injection 방지가 구현되어 있다 (ORM 사용)
- [ ] 민감 정보가 환경변수로 관리된다 (.env 파일)

---

#### Story 3.3: 가용성 요구사항
**Epic**: Epic 3 (비기능 요구사항)  
**Size**: S  
**Priority**: High

**Implementation Scope**:
- 에러 로깅 (파일 로깅)
- 사용자 친화적 에러 메시지
- 세션 만료 알림
- 네트워크 에러 재시도

**Acceptance Criteria**:
- [ ] 에러 발생 시 파일 로깅이 수행된다
- [ ] 에러 메시지가 사용자 친화적으로 표시된다
- [ ] 세션 만료 시 사용자에게 알림이 표시된다
- [ ] 네트워크 에러 시 재시도 메커니즘이 있다

---

### Backend Service Summary
- **Total Stories**: 3
- **Total Size**: 2M + 1S
- **Focus**: 비기능 요구사항 (성능, 보안, 가용성)
- **Dependencies**: None (독립적)

---

## Unit 2: Customer Frontend

### Assigned Stories (5 stories)

#### Story 1.1: 테이블 자동 로그인
**Epic**: Epic 1 (고객 주문 여정)  
**Size**: M  
**Priority**: High

**Implementation Scope**:
- 테이블 초기 설정 화면
- LocalStorage에 로그인 정보 저장
- 자동 로그인 로직
- 세션 만료 처리 (16시간 OR 마지막 주문 후 일정 시간)

**Acceptance Criteria**:
- [ ] 관리자가 테이블 태블릿을 초기 설정할 수 있다
- [ ] 초기 설정 후 로그인 정보가 LocalStorage에 저장된다
- [ ] 브라우저 재시작 시 저장된 정보로 자동 로그인된다
- [ ] 자동 로그인 성공 시 메뉴 화면으로 이동한다
- [ ] 로그인 실패 시 에러 메시지가 표시된다
- [ ] 테이블 세션이 만료되면 자동 로그아웃된다

**Dependencies**: None

---

#### Story 1.2: 메뉴 조회 및 탐색
**Epic**: Epic 1 (고객 주문 여정)  
**Size**: L  
**Priority**: High

**Implementation Scope**:
- 메뉴 목록 화면 (카드 레이아웃)
- 카테고리별 필터링
- 메뉴 상세 모달
- 터치 친화적 UI

**Acceptance Criteria**:
- [ ] 메뉴 화면이 기본 화면으로 표시된다
- [ ] 카테고리별로 메뉴가 분류되어 표시된다
- [ ] 각 메뉴에 메뉴명, 가격, 이미지가 표시된다
- [ ] 메뉴 카드를 클릭하면 상세 정보가 표시된다
- [ ] 카테고리 간 빠른 이동이 가능하다
- [ ] 터치 친화적인 UI (버튼 최소 44x44px)
- [ ] 메뉴 로딩 실패 시 에러 메시지가 표시된다

**Dependencies**: Story 1.1 (자동 로그인)

---

#### Story 1.3: 장바구니 관리
**Epic**: Epic 1 (고객 주문 여정)  
**Size**: M  
**Priority**: High

**Implementation Scope**:
- 장바구니 화면
- 수량 증가/감소 버튼
- 총 금액 계산
- LocalStorage 저장
- 세션 종료 시 장바구니 초기화

**Acceptance Criteria**:
- [ ] 메뉴 선택 시 장바구니에 추가된다
- [ ] 장바구니에서 메뉴 수량을 증가/감소할 수 있다
- [ ] 장바구니에서 메뉴를 삭제할 수 있다
- [ ] 총 금액이 실시간으로 계산되어 표시된다
- [ ] 장바구니 비우기 기능이 있다
- [ ] 장바구니 데이터가 LocalStorage에 저장된다
- [ ] 테이블 세션 종료 시 장바구니가 자동으로 비워진다

**Dependencies**: Story 1.2 (메뉴 조회)

---

#### Story 1.4: 주문 생성
**Epic**: Epic 1 (고객 주문 여정)  
**Size**: M  
**Priority**: High

**Implementation Scope**:
- 주문 확정 화면
- 주문 API 호출
- 주문 성공/실패 처리
- 장바구니 초기화

**Acceptance Criteria**:
- [ ] 장바구니에서 "주문하기" 버튼을 클릭할 수 있다
- [ ] 주문 확정 전 최종 확인 화면이 표시된다
- [ ] 주문 성공 시 주문 번호가 표시된다
- [ ] 주문 성공 시 장바구니가 자동으로 비워진다
- [ ] 주문 성공 후 메뉴 화면으로 자동 리다이렉트된다
- [ ] 주문 실패 시 에러 메시지가 표시되고 장바구니가 유지된다
- [ ] 주문 정보에 매장 ID, 테이블 ID, 세션 ID, 메뉴 목록, 총 금액이 포함된다

**Dependencies**: Story 1.3 (장바구니 관리)

---

#### Story 1.5: 주문 내역 조회
**Epic**: Epic 1 (고객 주문 여정)  
**Size**: S  
**Priority**: High

**Implementation Scope**:
- 주문 내역 화면
- 현재 세션 주문만 필터링
- 주문 상태 표시

**Acceptance Criteria**:
- [ ] "주문 내역" 메뉴를 통해 주문 내역 화면으로 이동할 수 있다
- [ ] 현재 테이블 세션의 주문만 표시된다
- [ ] 주문 시간 순으로 정렬되어 표시된다
- [ ] 각 주문에 주문 번호, 시각, 메뉴 목록, 금액, 상태가 표시된다
- [ ] 주문 상태가 표시된다 (대기중/준비중/완료)
- [ ] 매장 이용 완료 처리된 주문은 표시되지 않는다

**Dependencies**: Story 1.4 (주문 생성)

---

### Customer Frontend Summary
- **Total Stories**: 5
- **Total Size**: 1L + 3M + 1S
- **Focus**: 고객 주문 여정 (테이블 로그인 → 메뉴 조회 → 장바구니 → 주문 → 내역)
- **Dependencies**: Backend Service (API)

---

## Unit 3: Admin Frontend

### Assigned Stories (4 stories)

#### Story 2.1: 매장 인증
**Epic**: Epic 2 (관리자 운영 여정)  
**Size**: M  
**Priority**: High

**Implementation Scope**:
- 관리자 로그인 화면
- JWT 토큰 LocalStorage 저장
- 16시간 세션 유지
- 자동 로그아웃

**Acceptance Criteria**:
- [ ] 매장 식별자, 사용자명, 비밀번호를 입력하여 로그인할 수 있다
- [ ] 로그인 성공 시 JWT 토큰이 발급된다
- [ ] JWT 토큰이 LocalStorage에 저장된다
- [ ] 16시간 동안 세션이 유지된다
- [ ] 브라우저 새로고침 시에도 세션이 유지된다
- [ ] 16시간 후 자동 로그아웃된다
- [ ] 로그인 실패 시 에러 메시지가 표시된다
- [ ] 비밀번호는 bcrypt로 해싱되어 저장된다

**Dependencies**: None

---

#### Story 2.2: 실시간 주문 모니터링
**Epic**: Epic 2 (관리자 운영 여정)  
**Size**: XL  
**Priority**: High

**Implementation Scope**:
- 주문 대시보드 (테이블별 카드)
- SSE 연결 및 실시간 업데이트
- 주문 상태 변경
- 신규 주문 강조

**Acceptance Criteria**:
- [ ] 관리자 대시보드에 테이블별 카드 형태로 주문이 표시된다
- [ ] 각 테이블 카드에 총 주문액이 표시된다
- [ ] 각 테이블 카드에 최신 주문 n개가 미리보기로 표시된다
- [ ] 테이블 카드 클릭 시 전체 주문 목록이 상세 보기로 표시된다
- [ ] 신규 주문이 들어오면 실시간으로 업데이트된다 (SSE 사용)
- [ ] 신규 주문이 시각적으로 강조된다
- [ ] 주문 상태를 변경할 수 있다 (대기중 → 준비중 → 완료)
- [ ] 주문 상태 변경 시 즉시 반영된다
- [ ] 실시간 업데이트가 2초 이내에 표시된다

**Dependencies**: Story 2.1 (매장 인증)

---

#### Story 2.3: 테이블 관리
**Epic**: Epic 2 (관리자 운영 여정)  
**Size**: L  
**Priority**: High

**Implementation Scope**:
- 테이블 초기 설정
- 주문 삭제
- 테이블 세션 종료
- 과거 주문 내역 조회

**Acceptance Criteria**:
- [ ] 테이블 태블릿 초기 설정을 할 수 있다
- [ ] 특정 주문을 삭제할 수 있다 (확인 팝업 표시)
- [ ] 주문 삭제 시 테이블 총 주문액이 재계산된다
- [ ] 테이블 세션을 종료할 수 있다 ("매장 이용 완료" 처리)
- [ ] 세션 종료 시 확인 팝업이 표시된다
- [ ] 세션 종료 시 해당 세션의 주문 내역이 과거 이력으로 이동한다
- [ ] 세션 종료 시 테이블 현재 주문 목록 및 총 주문액이 0으로 리셋된다
- [ ] 과거 주문 내역을 조회할 수 있다 (테이블별, 날짜 필터링)
- [ ] 과거 내역에 주문 번호, 시각, 메뉴 목록, 총 금액, 완료 시각이 표시된다

**Dependencies**: Story 2.2 (실시간 주문 모니터링)

---

#### Story 2.4: 메뉴 관리
**Epic**: Epic 2 (관리자 운영 여정)  
**Size**: L  
**Priority**: High

**Implementation Scope**:
- 메뉴 목록 화면
- 메뉴 CRUD (생성, 조회, 수정, 삭제)
- 이미지 업로드
- 메뉴 순서 조정

**Acceptance Criteria**:
- [ ] 메뉴 목록을 카테고리별로 조회할 수 있다
- [ ] 새 메뉴를 등록할 수 있다
- [ ] 메뉴 이미지를 서버에 업로드할 수 있다
- [ ] 기존 메뉴를 수정할 수 있다
- [ ] 메뉴를 삭제할 수 있다 (확인 팝업 표시)
- [ ] 메뉴 노출 순서를 조정할 수 있다
- [ ] 필수 필드가 비어있으면 에러 메시지가 표시된다
- [ ] 가격은 양수여야 한다

**Dependencies**: Story 2.1 (매장 인증)

---

### Admin Frontend Summary
- **Total Stories**: 4
- **Total Size**: 1XL + 2L + 1M
- **Focus**: 관리자 운영 여정 (인증 → 주문 모니터링 → 테이블 관리 → 메뉴 관리)
- **Dependencies**: Backend Service (API + SSE)

---

## Story Dependencies Across Units

### Cross-Unit Dependencies

#### Backend Service → Customer Frontend
- Backend API가 완성되어야 Customer Frontend 개발 가능
- 필요한 API:
  - `/api/auth/table-login`
  - `/api/menus`
  - `/api/orders`

#### Backend Service → Admin Frontend
- Backend API + SSE가 완성되어야 Admin Frontend 개발 가능
- 필요한 API:
  - `/api/auth/admin-login`
  - `/api/admin/orders`
  - `/api/admin/tables`
  - `/api/admin/menus`
  - `/api/admin/sse/orders`

#### Customer Frontend ↔ Admin Frontend
- 직접적인 의존성 없음
- 병렬 개발 가능 (Backend 완성 후)

---

## Development Sequence

### Phase 1: Backend Service (Unit 1)
**Stories**: 3.1, 3.2, 3.3

**Order**:
1. Story 3.2 (보안 요구사항) - 인증 기반 구축
2. Story 3.1 (성능 요구사항) - API 최적화
3. Story 3.3 (가용성 요구사항) - 에러 처리

**Output**: 완전히 동작하는 Backend API

---

### Phase 2: Customer Frontend (Unit 2)
**Stories**: 1.1, 1.2, 1.3, 1.4, 1.5

**Order** (순차적 의존성):
1. Story 1.1 (테이블 자동 로그인)
2. Story 1.2 (메뉴 조회 및 탐색)
3. Story 1.3 (장바구니 관리)
4. Story 1.4 (주문 생성)
5. Story 1.5 (주문 내역 조회)

**Output**: 고객용 주문 앱

---

### Phase 3: Admin Frontend (Unit 3)
**Stories**: 2.1, 2.2, 2.3, 2.4

**Order**:
1. Story 2.1 (매장 인증)
2. Story 2.2 (실시간 주문 모니터링) - 핵심 기능
3. Story 2.4 (메뉴 관리) - 독립적
4. Story 2.3 (테이블 관리) - Story 2.2 의존

**Output**: 관리자용 운영 앱

---

## Story Complexity by Unit

| Unit | Small (S) | Medium (M) | Large (L) | Extra Large (XL) | Total |
|------|-----------|------------|-----------|------------------|-------|
| Backend Service | 1 | 2 | 0 | 0 | 3 |
| Customer Frontend | 1 | 3 | 1 | 0 | 5 |
| Admin Frontend | 0 | 1 | 2 | 1 | 4 |
| **Total** | **2** | **6** | **3** | **1** | **12** |

---

## Validation

### All Stories Assigned
✅ 12개 Stories 모두 Unit에 할당됨

### No Duplicate Assignments
✅ 각 Story는 정확히 하나의 Unit에만 할당됨

### Dependencies Respected
✅ Unit 간 의존성이 개발 순서에 반영됨

### Balanced Distribution
✅ 각 Unit이 적절한 수의 Stories를 가짐 (3-5개)

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
