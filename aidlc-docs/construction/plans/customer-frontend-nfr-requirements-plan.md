# NFR Requirements Plan - Customer Frontend

## Unit Context

**Unit Name**: Customer Frontend  
**Unit Type**: Frontend Application (Vue.js 3)  
**Project Type**: Greenfield

**Assigned Stories** (5 stories):
- Story 1.1: 테이블 자동 로그인
- Story 1.2: 메뉴 조회 및 탐색
- Story 1.3: 장바구니 관리
- Story 1.4: 주문 생성
- Story 1.5: 주문 내역 조회

**Dependencies**: Backend Service (API)

---

## NFR Requirements Questions

Frontend 애플리케이션의 비기능 요구사항을 결정하기 위한 질문입니다. 초보자 친화적 답변을 AI가 추천하고 적용할 예정입니다.

### Q1. 성능 목표 - 페이지 로딩 시간

메뉴 화면 등 주요 페이지의 초기 로딩 시간 목표는?

**A) 빠름 (< 1초)**
- 매우 빠른 사용자 경험
- 최적화 노력 많이 필요
- 번들 크기 최소화, 코드 스플리팅 필수

**B) 표준 (< 2초)**
- 일반적인 웹 앱 수준
- 적절한 최적화로 달성 가능
- 권장 목표

**C) 여유 (< 3초)**
- 느린 네트워크 환경 고려
- 최적화 부담 적음
- 사용자 경험 저하 가능

[Answer]: B

---

### Q2. 성능 목표 - API 응답 대기 시간

API 호출 후 UI 업데이트까지 허용 가능한 시간은?

**A) 즉시 (< 500ms)**
- 매우 빠른 반응
- Backend 성능 의존
- 로딩 스피너 최소화

**B) 빠름 (< 1초)**
- 일반적인 웹 앱 수준
- 로딩 스피너 표시
- 권장 목표

**C) 표준 (< 2초)**
- 느린 네트워크 고려
- 로딩 스피너 필수
- 사용자 인내심 필요

[Answer]: B

---

### Q3. 오프라인 지원

네트워크 연결이 끊겼을 때 어떻게 동작할까요?

**A) 오프라인 모드 지원**
- Service Worker 사용
- 캐시된 데이터로 동작
- 복잡한 구현

**B) 에러 메시지만 표시**
- 네트워크 에러 알림
- 재시도 버튼 제공
- 간단한 구현 (권장)

**C) 아무 처리 안 함**
- 사용자가 알아서 판단
- 권장하지 않음

[Answer]: B

---

### Q4. 브라우저 호환성

어떤 브라우저를 지원할까요?

**A) 최신 브라우저만 (Modern)**
- Chrome, Firefox, Safari, Edge 최신 버전
- ES6+ 문법 사용 가능
- 개발 간편 (권장)

**B) 최신 + 1년 전 버전**
- 약간의 Polyfill 필요
- 더 넓은 사용자 지원

**C) IE11 포함**
- 많은 Polyfill 필요
- 개발 복잡도 증가
- 권장하지 않음

[Answer]: A

---

### Q5. 반응형 디자인

다양한 화면 크기를 지원할까요?

**A) 태블릿 전용 (고정 크기)**
- 특정 해상도에 최적화
- 간단한 구현
- 테이블 태블릿 전용이므로 권장

**B) 반응형 (Responsive)**
- 다양한 화면 크기 지원
- 미디어 쿼리 사용
- 복잡한 구현

**C) 적응형 (Adaptive)**
- 특정 브레이크포인트만 지원
- 중간 복잡도

[Answer]: A

---

### Q6. 접근성 (Accessibility)

웹 접근성 표준을 준수할까요?

**A) 기본 접근성만**
- 시맨틱 HTML 사용
- alt 텍스트 제공
- 간단한 구현 (권장)

**B) WCAG 2.1 AA 준수**
- 키보드 네비게이션
- 스크린 리더 지원
- 색상 대비 준수
- 복잡한 구현

**C) 접근성 고려 안 함**
- 권장하지 않음

[Answer]: A

---

### Q7. 상태 관리 복잡도

Pinia Store의 구조를 어떻게 설계할까요?

**A) 단순 구조 (Simple)**
- 4개 Store (auth, menu, cart, order)
- 각 Store는 독립적
- 간단한 구현 (권장)

**B) 모듈화 구조 (Modular)**
- Store 간 의존성 관리
- 공통 로직 추출
- 중간 복잡도

**C) 복잡한 구조 (Complex)**
- Vuex 패턴 적용
- Actions, Mutations 분리
- 높은 복잡도

[Answer]: A

---

### Q8. 에러 로깅

에러 발생 시 로깅을 어떻게 할까요?

**A) 콘솔 로그만 (Console)**
- console.error() 사용
- 개발 중 디버깅 용이
- 프로덕션 로그 없음 (권장)

**B) 로컬 스토리지 저장**
- LocalStorage에 에러 로그 저장
- 사용자가 직접 확인 가능
- 중간 복잡도

**C) 외부 서비스 (Sentry 등)**
- 실시간 에러 모니터링
- 알림 기능
- 추가 비용 및 설정 필요

[Answer]: A

---

### Q9. 번들 크기 최적화

JavaScript 번들 크기를 어떻게 관리할까요?

**A) 기본 최적화만**
- Vite 기본 설정 사용
- Tree-shaking 자동 적용
- 간단한 구현 (권장)

**B) 코드 스플리팅**
- 라우트별 청크 분리
- 동적 import 사용
- 중간 복잡도

**C) 적극적 최적화**
- 모든 라이브러리 최적화
- 번들 분석 도구 사용
- 높은 복잡도

[Answer]: A

---

### Q10. 보안 - XSS 방어

Cross-Site Scripting (XSS) 공격을 어떻게 방어할까요?

**A) Vue.js 기본 보호**
- Vue.js의 자동 이스케이핑 사용
- v-html 사용 금지
- 간단한 구현 (권장)

**B) 추가 보안 라이브러리**
- DOMPurify 등 사용
- 입력 검증 강화
- 중간 복잡도

**C) CSP (Content Security Policy)**
- HTTP 헤더 설정
- 인라인 스크립트 금지
- 높은 복잡도

[Answer]: A

---

## Execution Plan

### Phase 1: Analyze Functional Design
- [x] Functional Design 아티팩트 읽기
- [x] 비즈니스 로직 복잡도 이해

### Phase 2: Create NFR Requirements Plan
- [x] 10개 NFR 질문 생성
- [x] 각 질문에 초보자 친화적 옵션 제공
- [x] Plan 파일 저장

### Phase 3: Collect Answers
- [x] 사용자 답변 수집
- [x] 답변 검토 및 모순 확인
- [x] 필요 시 명확화 질문 생성

### Phase 4: Generate NFR Requirements Artifacts
- [x] nfr-requirements.md 생성
- [x] tech-stack-decisions.md 생성

### Phase 5: Present and Approve
- [x] 완료 메시지 표시
- [x] 사용자 승인 대기
- [x] audit.md 로깅

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 답변 대기
