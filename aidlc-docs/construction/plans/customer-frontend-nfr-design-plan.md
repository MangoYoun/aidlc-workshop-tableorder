# NFR Design Plan - Customer Frontend

## Unit Context

**Unit Name**: Customer Frontend  
**Unit Type**: Frontend Application (Vue.js 3)  
**Project Type**: Greenfield

**NFR Requirements Summary**:
- 성능: 페이지 로딩 < 2초, API 응답 < 1초, 번들 크기 < 500KB
- 가용성: 네트워크 에러 처리, 로딩 상태 표시
- 보안: XSS 방어, 세션 토큰 보안
- 사용성: 터치 친화적 UI, 사용자 피드백

**Tech Stack**:
- Vue.js 3.4+, Vite 5.0+, Pinia 2.1+
- Axios 1.6+, Tailwind CSS 3.4+

---

## NFR Design Questions

Frontend 애플리케이션의 NFR 설계를 위한 질문입니다. 초보자 친화적 답변을 AI가 추천하고 적용할 예정입니다.

### Q1. 성능 최적화 - 컴포넌트 로딩 전략

Vue 컴포넌트를 어떻게 로딩할까요?

**A) 동기 로딩 (Synchronous)**
- 모든 컴포넌트를 초기에 로딩
- 간단한 구현
- 초기 번들 크기 증가 (권장 - 프로젝트 규모 작음)

**B) 라우트별 코드 스플리팅**
- 라우트별로 청크 분리
- 초기 로딩 빠름
- 중간 복잡도

**C) 컴포넌트별 Lazy Loading**
- 모든 컴포넌트 동적 로딩
- 최소 초기 번들
- 높은 복잡도

[Answer]: A

---

### Q2. 성능 최적화 - 이미지 로딩 전략

메뉴 이미지를 어떻게 로딩할까요?

**A) 즉시 로딩 (Eager)**
- 모든 이미지 즉시 로딩
- 간단한 구현
- 초기 로딩 느림 (권장 - 이미지 수 적음)

**B) Lazy Loading**
- 스크롤 시 이미지 로딩
- 초기 로딩 빠름
- Intersection Observer 사용

**C) Progressive Loading**
- 저화질 → 고화질 순차 로딩
- 부드러운 UX
- 복잡한 구현

[Answer]: A

---

### Q3. 상태 관리 - Store 간 통신

Pinia Store 간 데이터 공유를 어떻게 할까요?

**A) 직접 참조 (Direct Reference)**
- Store에서 다른 Store 직접 import
- 간단한 구현
- 순환 참조 주의 (권장)

**B) 이벤트 버스 (Event Bus)**
- 중앙 이벤트 시스템
- 느슨한 결합
- 추가 복잡도

**C) 완전 독립 (Fully Independent)**
- Store 간 통신 없음
- 데이터 중복 가능
- 가장 간단

[Answer]: C

---

### Q4. 에러 처리 - 전역 에러 핸들러

Vue 앱의 에러를 어떻게 처리할까요?

**A) 전역 에러 핸들러만**
- `app.config.errorHandler` 사용
- 모든 에러 중앙 처리
- 간단한 구현 (권장)

**B) 전역 + 컴포넌트별**
- 전역 핸들러 + try-catch
- 세밀한 제어
- 중간 복잡도

**C) 에러 바운더리 (Error Boundary)**
- Vue 3 Suspense + ErrorBoundary
- React 스타일
- 높은 복잡도

[Answer]: A

---

### Q5. API 호출 - 중복 요청 방지

동일한 API를 여러 번 호출하는 것을 어떻게 방지할까요?

**A) 방지 안 함**
- 중복 호출 허용
- 간단한 구현
- Backend에서 처리 (권장)

**B) Request Deduplication**
- Axios Interceptor로 중복 제거
- 클라이언트 최적화
- 중간 복잡도

**C) Request Caching**
- 응답 캐싱
- 빠른 재호출
- 높은 복잡도

[Answer]: A

---

### Q6. 보안 - 민감 정보 보호

LocalStorage의 민감 정보를 어떻게 보호할까요?

**A) 암호화 안 함**
- 평문 저장
- 간단한 구현
- HTTPS로 충분 (권장)

**B) 클라이언트 암호화**
- CryptoJS 등 사용
- 추가 보안
- 중간 복잡도

**C) SessionStorage 사용**
- 탭 닫으면 삭제
- 보안 강화
- 자동 로그인 불가

[Answer]: A

---

### Q7. 사용성 - 로딩 상태 관리

여러 API 호출 시 로딩 상태를 어떻게 관리할까요?

**A) 개별 로딩 상태**
- 각 API마다 별도 loading 변수
- 세밀한 제어
- 간단한 구현 (권장)

**B) 전역 로딩 상태**
- 하나의 전역 loading 변수
- 단순한 UI
- 동시 호출 시 문제

**C) 로딩 카운터**
- 진행 중인 요청 수 추적
- 정확한 상태
- 중간 복잡도

[Answer]: A

---

### Q8. 사용성 - 토스트 메시지 관리

토스트 메시지를 어떻게 관리할까요?

**A) 간단한 컴포넌트**
- 자체 구현 Toast 컴포넌트
- 커스터마이징 용이
- 간단한 구현 (권장)

**B) 라이브러리 사용**
- vue-toastification 등
- 풍부한 기능
- 추가 의존성

**C) 브라우저 알림**
- window.alert() 사용
- 가장 간단
- UX 저하

[Answer]: A

---

### Q9. 반응성 - 대용량 리스트 렌더링

메뉴 목록(100개)을 어떻게 렌더링할까요?

**A) 일반 렌더링**
- v-for로 전체 렌더링
- 간단한 구현
- 100개 정도는 문제없음 (권장)

**B) 가상 스크롤 (Virtual Scroll)**
- 보이는 영역만 렌더링
- 성능 최적화
- 복잡한 구현

**C) 페이지네이션**
- 10개씩 페이지 분할
- 서버 부하 감소
- 추가 UI 필요

[Answer]: A

---

### Q10. 개발 도구 - 디버깅 지원

개발 중 디버깅을 어떻게 지원할까요?

**A) Vue DevTools만**
- 브라우저 확장 프로그램
- 충분한 기능
- 추가 설정 불필요 (권장)

**B) Vue DevTools + 커스텀 로깅**
- 추가 로깅 유틸리티
- 상세한 디버깅
- 중간 복잡도

**C) 프로덕션 모니터링**
- Sentry 등 통합
- 실시간 에러 추적
- 추가 비용

[Answer]: A

---

## Execution Plan

### Phase 1: Analyze NFR Requirements
- [x] NFR Requirements 아티팩트 읽기
- [x] 성능, 보안, 사용성 요구사항 이해

### Phase 2: Create NFR Design Plan
- [x] 10개 NFR 설계 질문 생성
- [x] 각 질문에 초보자 친화적 옵션 제공
- [x] Plan 파일 저장

### Phase 3: Collect Answers
- [x] 사용자 답변 수집
- [x] 답변 검토 및 모순 확인
- [x] 필요 시 명확화 질문 생성

### Phase 4: Generate NFR Design Artifacts
- [x] nfr-design-patterns.md 생성
- [x] logical-components.md 생성

### Phase 5: Present and Approve
- [x] 완료 메시지 표시
- [x] 사용자 승인 대기
- [x] audit.md 로깅

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 답변 대기
