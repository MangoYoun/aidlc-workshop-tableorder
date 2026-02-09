# User Stories

## Epic 1: 고객 주문 여정 (Customer Ordering Journey)

**Epic Description**: 고객이 테이블에 앉아서 메뉴를 조회하고, 주문하고, 주문 내역을 확인하는 전체 여정

**Size**: XL

---

### Story 1.1: 테이블 자동 로그인

**As a** 고객  
**I want** 테이블 태블릿이 자동으로 로그인되어 있기를  
**So that** 별도의 로그인 절차 없이 즉시 주문을 시작할 수 있다

**Size**: M

**Acceptance Criteria**:
- [ ] 관리자가 테이블 태블릿을 초기 설정할 수 있다 (매장 ID, 테이블 번호, 비밀번호)
- [ ] 초기 설정 후 로그인 정보가 LocalStorage에 저장된다
- [ ] 브라우저 재시작 시 저장된 정보로 자동 로그인된다
- [ ] 자동 로그인 성공 시 메뉴 화면으로 이동한다
- [ ] 로그인 실패 시 에러 메시지가 표시된다
- [ ] 테이블 세션이 만료되면 (16시간 OR 마지막 주문 후 일정 시간) 자동 로그아웃된다

**Dependencies**: None

**Notes**:
- 테이블 세션 만료 정책: 16시간 고정 OR 마지막 주문 후 일정 시간 (예: 2시간)
- LocalStorage 사용으로 브라우저 닫아도 로그인 유지

---

### Story 1.2: 메뉴 조회 및 탐색

**As a** 고객  
**I want** 매장의 메뉴를 카테고리별로 조회하고 상세 정보를 확인하기를  
**So that** 원하는 메뉴를 쉽게 찾고 선택할 수 있다

**Size**: L

**Acceptance Criteria**:
- [ ] 메뉴 화면이 기본 화면으로 표시된다
- [ ] 카테고리별로 메뉴가 분류되어 표시된다
- [ ] 각 메뉴에 메뉴명, 가격, 이미지가 표시된다
- [ ] 메뉴 카드를 클릭하면 상세 정보(설명 포함)가 표시된다
- [ ] 카테고리 간 빠른 이동이 가능하다
- [ ] 터치 친화적인 UI (버튼 최소 44x44px)
- [ ] 메뉴 로딩 실패 시 에러 메시지가 표시된다

**Dependencies**: Story 1.1 (자동 로그인)

**Notes**:
- 카드 형태의 메뉴 레이아웃
- 메뉴 이미지는 서버에 저장된 이미지 사용

---

### Story 1.3: 장바구니 관리

**As a** 고객  
**I want** 선택한 메뉴를 장바구니에 담고 수량을 조절하기를  
**So that** 주문 전에 메뉴를 검토하고 수정할 수 있다

**Size**: M

**Acceptance Criteria**:
- [ ] 메뉴 선택 시 장바구니에 추가된다
- [ ] 장바구니에서 메뉴 수량을 증가/감소할 수 있다
- [ ] 장바구니에서 메뉴를 삭제할 수 있다
- [ ] 총 금액이 실시간으로 계산되어 표시된다
- [ ] 장바구니 비우기 기능이 있다
- [ ] 장바구니 데이터가 LocalStorage에 저장된다 (페이지 새로고침 시에도 유지)
- [ ] 테이블 세션 종료 시 장바구니가 자동으로 비워진다

**Dependencies**: Story 1.2 (메뉴 조회)

**Notes**:
- LocalStorage 사용으로 새로고침 시에도 장바구니 유지
- 테이블 세션 종료 시 다음 고객을 위해 장바구니 초기화

---

### Story 1.4: 주문 생성

**As a** 고객  
**I want** 장바구니의 메뉴를 주문으로 확정하기를  
**So that** 선택한 메뉴를 주방에 전달하고 조리를 시작할 수 있다

**Size**: M

**Acceptance Criteria**:
- [ ] 장바구니에서 "주문하기" 버튼을 클릭할 수 있다
- [ ] 주문 확정 전 최종 확인 화면이 표시된다
- [ ] 주문 성공 시 주문 번호가 표시된다
- [ ] 주문 성공 시 장바구니가 자동으로 비워진다
- [ ] 주문 성공 후 메뉴 화면으로 자동 리다이렉트된다
- [ ] 주문 실패 시 에러 메시지가 표시되고 장바구니가 유지된다
- [ ] 주문 정보에 매장 ID, 테이블 ID, 세션 ID, 메뉴 목록, 총 금액이 포함된다

**Dependencies**: Story 1.3 (장바구니 관리)

**Notes**:
- 주문 성공 시 5초간 주문 번호 표시 후 자동 리다이렉트
- 추가 주문을 위해 메뉴 화면으로 복귀

---

### Story 1.5: 주문 내역 조회

**As a** 고객  
**I want** 현재 테이블의 주문 내역을 확인하기를  
**So that** 내가 주문한 메뉴와 상태를 확인할 수 있다

**Size**: S

**Acceptance Criteria**:
- [ ] "주문 내역" 메뉴를 통해 주문 내역 화면으로 이동할 수 있다
- [ ] 현재 테이블 세션의 주문만 표시된다 (이전 세션 제외)
- [ ] 주문 시간 순으로 정렬되어 표시된다
- [ ] 각 주문에 주문 번호, 시각, 메뉴 목록, 금액, 상태가 표시된다
- [ ] 주문 상태가 표시된다 (대기중/준비중/완료)
- [ ] 매장 이용 완료 처리된 주문은 표시되지 않는다

**Dependencies**: Story 1.4 (주문 생성)

**Notes**:
- 현재 세션의 주문만 표시 (과거 고객의 주문 제외)
- 실시간 상태 업데이트는 선택사항 (MVP에서는 수동 새로고침)

---

## Epic 2: 관리자 운영 여정 (Admin Operations Journey)

**Epic Description**: 관리자가 매장에 로그인하여 실시간으로 주문을 모니터링하고, 테이블과 메뉴를 관리하는 전체 여정

**Size**: XL

---

### Story 2.1: 매장 인증

**As a** 관리자  
**I want** 매장 관리 시스템에 로그인하기를  
**So that** 주문 관리 및 매장 운영 기능에 접근할 수 있다

**Size**: M

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

**Notes**:
- JWT 토큰 LocalStorage 저장으로 새로고침 시에도 세션 유지
- 보안: 비밀번호 bcrypt 해싱, 로그인 시도 제한

---

### Story 2.2: 실시간 주문 모니터링

**As a** 관리자  
**I want** 들어오는 주문을 실시간으로 확인하고 상태를 변경하기를  
**So that** 주문을 효율적으로 처리하고 고객에게 빠른 서비스를 제공할 수 있다

**Size**: XL

**Acceptance Criteria**:
- [ ] 관리자 대시보드에 테이블별 카드 형태로 주문이 표시된다
- [ ] 각 테이블 카드에 총 주문액이 표시된다
- [ ] 각 테이블 카드에 최신 주문 n개가 미리보기로 표시된다
- [ ] 테이블 카드 클릭 시 전체 주문 목록이 상세 보기로 표시된다
- [ ] 신규 주문이 들어오면 실시간으로 업데이트된다 (SSE 사용)
- [ ] 신규 주문이 시각적으로 강조된다 (색상 변경, 애니메이션)
- [ ] 주문 상태를 변경할 수 있다 (대기중 → 준비중 → 완료)
- [ ] 주문 상태 변경 시 즉시 반영된다
- [ ] 실시간 업데이트가 2초 이내에 표시된다

**Dependencies**: Story 2.1 (매장 인증)

**Notes**:
- Server-Sent Events (SSE) 사용으로 실시간 통신
- 그리드 레이아웃으로 테이블별 주문 현황 한눈에 파악

---

### Story 2.3: 테이블 관리

**As a** 관리자  
**I want** 테이블 세션을 관리하고 주문을 수정하기를  
**So that** 테이블 상태를 효율적으로 관리하고 필요 시 주문을 조정할 수 있다

**Size**: L

**Acceptance Criteria**:
- [ ] 테이블 태블릿 초기 설정을 할 수 있다 (테이블 번호, 비밀번호)
- [ ] 특정 주문을 삭제할 수 있다 (확인 팝업 표시)
- [ ] 주문 삭제 시 테이블 총 주문액이 재계산된다
- [ ] 테이블 세션을 종료할 수 있다 ("매장 이용 완료" 처리)
- [ ] 세션 종료 시 확인 팝업이 표시된다
- [ ] 세션 종료 시 해당 세션의 주문 내역이 과거 이력으로 이동한다
- [ ] 세션 종료 시 테이블 현재 주문 목록 및 총 주문액이 0으로 리셋된다
- [ ] 과거 주문 내역을 조회할 수 있다 (테이블별, 날짜 필터링)
- [ ] 과거 내역에 주문 번호, 시각, 메뉴 목록, 총 금액, 완료 시각이 표시된다

**Dependencies**: Story 2.2 (실시간 주문 모니터링)

**Notes**:
- 테이블 세션 자동 종료: 16시간 OR 마지막 주문 후 일정 시간
- 과거 이력은 OrderHistory 테이블에 저장

---

### Story 2.4: 메뉴 관리

**As a** 관리자  
**I want** 메뉴를 추가, 수정, 삭제하기를  
**So that** 메뉴 정보를 최신 상태로 유지하고 고객에게 정확한 정보를 제공할 수 있다

**Size**: L

**Acceptance Criteria**:
- [ ] 메뉴 목록을 카테고리별로 조회할 수 있다
- [ ] 새 메뉴를 등록할 수 있다 (메뉴명, 가격, 설명, 카테고리, 이미지)
- [ ] 메뉴 이미지를 서버에 업로드할 수 있다
- [ ] 기존 메뉴를 수정할 수 있다
- [ ] 메뉴를 삭제할 수 있다 (확인 팝업 표시)
- [ ] 메뉴 노출 순서를 조정할 수 있다
- [ ] 필수 필드가 비어있으면 에러 메시지가 표시된다
- [ ] 가격은 양수여야 한다

**Dependencies**: Story 2.1 (매장 인증)

**Notes**:
- 메뉴 이미지는 서버에 업로드 및 저장
- CRUD 기능 모두 포함

---

## Epic 3: 비기능 요구사항 (Non-Functional Requirements)

**Epic Description**: 시스템의 성능, 보안, 가용성 등 비기능적 요구사항

**Size**: L

---

### Story 3.1: 성능 요구사항

**As a** 시스템  
**I want** 빠른 응답 속도와 안정적인 성능을 제공하기를  
**So that** 사용자가 원활하게 서비스를 이용할 수 있다

**Size**: M

**Acceptance Criteria**:
- [ ] API 응답 시간이 500ms 이하이다
- [ ] 페이지 로딩 시간이 2초 이내이다
- [ ] 실시간 주문 업데이트가 2초 이내에 표시된다
- [ ] 동시 사용자 10-50명을 지원한다
- [ ] 데이터베이스 쿼리가 최적화되어 있다

**Dependencies**: All functional stories

**Notes**:
- 성능 테스트 필요
- 중소규모 매장 3-10개 지원

---

### Story 3.2: 보안 요구사항

**As a** 시스템  
**I want** 안전한 인증 및 데이터 보호를 제공하기를  
**So that** 사용자 정보와 매장 데이터가 안전하게 보호된다

**Size**: M

**Acceptance Criteria**:
- [ ] JWT 기반 인증이 구현되어 있다
- [ ] 비밀번호가 bcrypt로 해싱되어 저장된다
- [ ] 로그인 시도 제한이 구현되어 있다
- [ ] 관리자 전용 기능에 권한 검증이 있다
- [ ] SQL Injection 방지가 구현되어 있다 (ORM 사용)
- [ ] 민감 정보가 환경변수로 관리된다 (.env 파일)

**Dependencies**: Story 2.1 (매장 인증), Story 1.1 (테이블 자동 로그인)

**Notes**:
- HTTPS 통신은 배포 시 적용
- AWS Secrets Manager 또는 환경변수 사용

---

### Story 3.3: 가용성 요구사항

**As a** 시스템  
**I want** 안정적인 에러 처리와 로깅을 제공하기를  
**So that** 장애 발생 시 빠르게 대응하고 복구할 수 있다

**Size**: S

**Acceptance Criteria**:
- [ ] 에러 발생 시 파일 로깅이 수행된다
- [ ] 에러 메시지가 사용자 친화적으로 표시된다
- [ ] 세션 만료 시 사용자에게 알림이 표시된다
- [ ] 네트워크 에러 시 재시도 메커니즘이 있다

**Dependencies**: All functional stories

**Notes**:
- 파일 로깅 사용
- 에러 복구 메커니즘 구현

---

## Story Summary

### Total Stories: 12
- Epic 1 (고객 주문 여정): 5 stories
- Epic 2 (관리자 운영 여정): 4 stories
- Epic 3 (비기능 요구사항): 3 stories

### Size Distribution:
- **S (Small)**: 2 stories
- **M (Medium)**: 6 stories
- **L (Large)**: 3 stories
- **XL (Extra Large)**: 1 story

### Priority (MVP):
- **Epic 1**: 모든 stories 필수
- **Epic 2**: 모든 stories 필수
- **Epic 3**: 모든 stories 필수

### Dependencies:
- Story 1.2 depends on Story 1.1
- Story 1.3 depends on Story 1.2
- Story 1.4 depends on Story 1.3
- Story 1.5 depends on Story 1.4
- Story 2.2 depends on Story 2.1
- Story 2.3 depends on Story 2.2
- Story 2.4 depends on Story 2.1
- Story 3.1 depends on all functional stories
- Story 3.2 depends on Story 2.1, Story 1.1
- Story 3.3 depends on all functional stories

---

## INVEST Criteria Verification

모든 User Stories는 INVEST 기준을 충족합니다:

- **Independent**: 각 Story는 독립적으로 구현 가능 (의존성은 명시됨)
- **Negotiable**: 구현 방법은 협의 가능
- **Valuable**: 각 Story는 사용자에게 명확한 가치 제공
- **Estimable**: 크기 추정 가능 (S/M/L/XL)
- **Small**: 각 Story는 적절한 크기로 분할됨
- **Testable**: 명확한 Acceptance Criteria로 테스트 가능
