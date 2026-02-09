# Infrastructure Design Plan - Customer Frontend

## Overview

Customer Frontend의 인프라 설계를 위한 실행 계획입니다. 정적 호스팅 및 배포 인프라를 결정합니다.

---

## Plan Steps

### Step 1: Analyze Design Artifacts
- [x] Read functional design from `aidlc-docs/construction/customer-frontend/functional-design/`
- [x] Read NFR design from `aidlc-docs/construction/customer-frontend/nfr-design/`
- [x] Identify logical components needing infrastructure

### Step 2: Create Infrastructure Design Plan
- [x] Generate plan with checkboxes for infrastructure design
- [x] Focus on mapping to actual services (AWS)

### Step 3: Generate Context-Appropriate Questions
- [x] Analyze functional and NFR design
- [x] Generate questions relevant to Customer Frontend infrastructure needs
- [x] Embed questions using [Answer]: tag format

### Step 4: Store Plan
- [x] Save as `aidlc-docs/construction/plans/customer-frontend-infrastructure-design-plan.md`

### Step 5: Collect and Analyze Answers
- [x] User selected beginner-friendly answers (all Option A)
- [x] No ambiguous responses detected

### Step 6: Generate Infrastructure Design Artifacts
- [x] Create `aidlc-docs/construction/customer-frontend/infrastructure-design/infrastructure-design.md`
- [x] Create `aidlc-docs/construction/customer-frontend/infrastructure-design/deployment-architecture.md`

### Step 7: Present Completion Message
- [x] Present completion message with review instructions
- [x] Wait for user approval

### Step 8: Wait for Explicit Approval
- [x] User reviews infrastructure design
- [x] User provides explicit approval

### Step 9: Record Approval and Update Progress
- [x] Log approval in audit.md with timestamp
- [x] Mark Infrastructure Design stage complete in aidlc-state.md

---

## Infrastructure Design Questions

### Q1. Deployment Environment
**Question**: Customer Frontend는 정적 파일(HTML, CSS, JS)로 빌드됩니다. 어떤 호스팅 방식을 선호하시나요?

**Options**:
- A) AWS S3 + CloudFront (정적 호스팅, CDN, 저렴한 비용)
- B) AWS Amplify Hosting (자동 배포, CI/CD 통합, 약간 높은 비용)
- C) EC2 + Nginx (서버 기반, 더 많은 제어, 높은 비용)

[Answer]: A

**Rationale**: 초보자 친화적, 비용 효율적, 정적 파일에 최적

---

### Q2. CDN (Content Delivery Network)
**Question**: 전 세계 사용자에게 빠른 콘텐츠 전송을 위해 CDN을 사용하시겠습니까?

**Options**:
- A) CloudFront 사용 (빠른 로딩, 캐싱, HTTPS 자동)
- B) CDN 없이 S3만 사용 (간단하지만 느린 로딩)

[Answer]: A

**Rationale**: 성능 향상, HTTPS 지원, 추가 비용 미미

---

### Q3. Domain Name (DNS)
**Question**: 커스텀 도메인 이름을 사용하시겠습니까?

**Options**:
- A) CloudFront URL 직접 사용 (예: d1234567890abc.cloudfront.net)
- B) Route 53으로 커스텀 도메인 설정 (예: tableorder.example.com)

[Answer]: A

**Rationale**: 초기 개발/테스트에는 CloudFront URL로 충분, 향후 추가 가능

---

### Q4. HTTPS/SSL
**Question**: HTTPS를 사용하시겠습니까?

**Options**:
- A) CloudFront 기본 HTTPS 사용 (무료, 자동 설정)
- B) HTTP만 사용 (보안 취약, 권장하지 않음)

[Answer]: A

**Rationale**: 보안 필수, CloudFront가 자동 지원

---

### Q5. Deployment Method
**Question**: 초기 배포 방식을 어떻게 하시겠습니까?

**Options**:
- A) 수동 배포 (AWS CLI로 S3 업로드)
- B) CI/CD 파이프라인 (GitHub Actions 자동 배포)

[Answer]: A

**Rationale**: 초기에는 수동 배포로 시작, 향후 CI/CD 추가 가능

---

### Q6. Environment Configuration
**Question**: 개발/프로덕션 환경을 분리하시겠습니까?

**Options**:
- A) 분리 (dev/prod 각각 S3 버킷)
- B) 단일 환경 (프로덕션만)

[Answer]: A

**Rationale**: 개발 환경에서 테스트 후 프로덕션 배포

---

### Q7. Caching Strategy
**Question**: CloudFront 캐싱 전략을 어떻게 설정하시겠습니까?

**Options**:
- A) 기본 캐싱 (HTML: 캐시 없음, JS/CSS: 1년, Images: 1주일)
- B) 커스텀 캐싱 (직접 설정)

[Answer]: A

**Rationale**: SPA에 최적화된 기본 전략

---

### Q8. Error Handling
**Question**: SPA 라우팅을 위한 에러 페이지 설정을 어떻게 하시겠습니까?

**Options**:
- A) 404/403 → index.html 리다이렉트 (SPA 라우팅 지원)
- B) 기본 에러 페이지 사용

[Answer]: A

**Rationale**: Vue Router가 클라이언트 측에서 라우팅 처리

---

### Q9. Monitoring
**Question**: 인프라 모니터링을 설정하시겠습니까?

**Options**:
- A) CloudWatch 기본 메트릭 사용 (요청 수, 에러율)
- B) 모니터링 없음

[Answer]: A

**Rationale**: 기본 모니터링으로 문제 감지

---

### Q10. Backup Strategy
**Question**: S3 버킷 백업 전략을 어떻게 하시겠습니까?

**Options**:
- A) S3 Versioning 활성화 (파일 변경 이력 보관, 롤백 가능)
- B) 백업 없음 (Git으로 관리)

[Answer]: A

**Rationale**: 실수로 삭제 시 복구 가능, 추가 비용 미미

---

## Answers Summary

| Question | Answer | Rationale |
|----------|--------|-----------|
| Q1. Deployment Environment | A (S3 + CloudFront) | 초보자 친화적, 비용 효율적 |
| Q2. CDN | A (CloudFront) | 성능 향상, HTTPS 지원 |
| Q3. Domain Name | A (CloudFront URL) | 초기에는 충분, 향후 추가 가능 |
| Q4. HTTPS/SSL | A (CloudFront HTTPS) | 보안 필수, 자동 지원 |
| Q5. Deployment Method | A (수동 배포) | 초기 간단한 방식 |
| Q6. Environment Configuration | A (dev/prod 분리) | 테스트 후 배포 |
| Q7. Caching Strategy | A (기본 캐싱) | SPA 최적화 |
| Q8. Error Handling | A (index.html 리다이렉트) | SPA 라우팅 지원 |
| Q9. Monitoring | A (CloudWatch) | 기본 모니터링 |
| Q10. Backup Strategy | A (S3 Versioning) | 롤백 가능 |

---

## Infrastructure Design Decisions

### 1. Hosting: AWS S3 + CloudFront
- 정적 파일 호스팅에 최적
- 비용 효율적 (~$2/월)
- 확장성 자동 지원

### 2. CDN: CloudFront
- 전 세계 빠른 로딩
- HTTPS 자동 지원
- 캐싱으로 성능 향상

### 3. Deployment: Manual → CI/CD
- 초기: AWS CLI로 수동 배포
- 향후: GitHub Actions 자동 배포

### 4. Environment: Dev/Prod 분리
- Dev: 개발 테스트 환경
- Prod: 프로덕션 환경

### 5. Monitoring: CloudWatch
- 요청 수, 에러율 모니터링
- 알림 설정 (선택사항)

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 진행 중 (Step 6 진행 중)
