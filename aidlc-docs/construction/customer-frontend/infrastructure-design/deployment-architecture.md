# Deployment Architecture - Customer Frontend

## Overview

Customer Frontend의 배포 아키텍처 및 배포 프로세스를 정의합니다.

---

## 1. Deployment Environments

### 1.1 Development Environment

**목적**: 개발 및 테스트

**인프라**:
```
S3 Bucket: tableorder-customer-frontend-dev
CloudFront: 선택사항 (비용 절감)
API URL: http://localhost:8000 (로컬 Backend)
```

**환경 변수** (`.env.development`):
```env
VITE_API_URL=http://localhost:8000
VITE_ENV=development
```

**접근 방법**:
- 로컬 개발: `npm run dev` (Vite Dev Server)
- S3 배포: AWS CLI로 수동 업로드 (선택사항)

---

### 1.2 Production Environment

**목적**: 실제 서비스 운영

**인프라**:
```
S3 Bucket: tableorder-customer-frontend-prod
CloudFront: 필수 (CDN, HTTPS)
API URL: https://api.tableorder.example.com (프로덕션 Backend)
```

**환경 변수** (`.env.production`):
```env
VITE_API_URL=https://api.tableorder.example.com
VITE_ENV=production
```

**접근 방법**:
- CloudFront URL: `https://d1234567890abc.cloudfront.net`
- 커스텀 도메인 (향후): `https://tableorder.example.com`

---

## 2. Deployment Process

### 2.1 Manual Deployment (초기)

**단계**:

#### Step 1: 로컬 빌드
```bash
# 프로덕션 빌드
npm run build

# 빌드 결과물 확인
ls -la dist/
```

**결과물**:
- `dist/index.html` - SPA 진입점
- `dist/assets/*.js` - JavaScript 번들
- `dist/assets/*.css` - CSS 번들
- `dist/images/` - 이미지 파일

---

#### Step 2: S3 업로드
```bash
# AWS CLI 설정 (최초 1회)
aws configure
# Access Key ID: [YOUR_ACCESS_KEY]
# Secret Access Key: [YOUR_SECRET_KEY]
# Region: ap-northeast-2

# S3 버킷 생성 (최초 1회)
aws s3 mb s3://tableorder-customer-frontend-prod --region ap-northeast-2

# 빌드 결과물 업로드
aws s3 sync dist/ s3://tableorder-customer-frontend-prod --delete

# --delete: S3에 있지만 로컬에 없는 파일 삭제
```

**업로드 시간**: 약 10-30초 (파일 크기에 따라)

---

#### Step 3: CloudFront 캐시 무효화
```bash
# CloudFront Distribution ID 확인 (최초 1회)
aws cloudfront list-distributions --query "DistributionList.Items[*].[Id,DomainName]" --output table

# 캐시 무효화 (모든 파일)
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"

# 무효화 상태 확인
aws cloudfront get-invalidation \
  --distribution-id E1234567890ABC \
  --id I1234567890ABC
```

**무효화 시간**: 약 1-5분

---

#### Step 4: 배포 확인
```bash
# CloudFront URL 접속
curl -I https://d1234567890abc.cloudfront.net

# 브라우저에서 확인
# https://d1234567890abc.cloudfront.net
```

**확인 사항**:
- HTTP 200 응답
- index.html 로드
- JavaScript/CSS 로드
- API 호출 정상 작동

---

### 2.2 CI/CD Pipeline (향후)

**도구**: GitHub Actions

**트리거**:
- `main` 브랜치에 푸시 시 자동 배포
- Pull Request 시 빌드 테스트만 수행

**워크플로우 파일** (`.github/workflows/deploy.yml`):
```yaml
name: Deploy to S3

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm run test
      
      - name: Build
        run: npm run build
        env:
          VITE_API_URL: ${{ secrets.VITE_API_URL }}
          VITE_ENV: production
      
      - name: Deploy to S3
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        run: |
          aws s3 sync dist/ s3://tableorder-customer-frontend-prod --delete
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: ap-northeast-2
      
      - name: Invalidate CloudFront cache
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.CF_DISTRIBUTION_ID }} \
            --paths "/*"
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: ap-northeast-2
      
      - name: Notify deployment
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        run: echo "Deployment complete!"
```

**GitHub Secrets 설정** (Settings → Secrets):
```
AWS_ACCESS_KEY_ID: [YOUR_ACCESS_KEY]
AWS_SECRET_ACCESS_KEY: [YOUR_SECRET_KEY]
CF_DISTRIBUTION_ID: E1234567890ABC
VITE_API_URL: https://api.tableorder.example.com
```

**배포 시간**: 약 3-5분 (빌드 + 업로드 + 무효화)

---

## 3. Rollback Strategy

### 3.1 S3 Versioning을 이용한 롤백

**전제 조건**: S3 Versioning 활성화

**단계**:

#### Step 1: 이전 버전 확인
```bash
# 특정 파일의 버전 목록 조회
aws s3api list-object-versions \
  --bucket tableorder-customer-frontend-prod \
  --prefix index.html

# 출력 예시:
# VersionId: abc123 (최신)
# VersionId: def456 (이전)
```

---

#### Step 2: 이전 버전 복원
```bash
# 특정 버전을 현재 버전으로 복사
aws s3api copy-object \
  --copy-source "tableorder-customer-frontend-prod/index.html?versionId=def456" \
  --bucket tableorder-customer-frontend-prod \
  --key index.html
```

---

#### Step 3: CloudFront 캐시 무효화
```bash
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"
```

**롤백 시간**: 약 2-5분

---

### 3.2 Git 태그를 이용한 롤백

**전제 조건**: Git 태그로 버전 관리

**단계**:

#### Step 1: 이전 버전 체크아웃
```bash
# 태그 목록 확인
git tag

# 이전 버전 체크아웃
git checkout v1.0.0
```

---

#### Step 2: 재빌드 및 배포
```bash
# 빌드
npm run build

# S3 업로드
aws s3 sync dist/ s3://tableorder-customer-frontend-prod --delete

# CloudFront 캐시 무효화
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"
```

---

#### Step 3: 원래 브랜치로 복귀
```bash
git checkout main
```

**롤백 시간**: 약 5-10분

---

## 4. Deployment Checklist

### Pre-Deployment Checklist

- [ ] 코드 변경 사항 리뷰 완료
- [ ] 로컬 테스트 통과 (`npm run test`)
- [ ] 로컬 빌드 성공 (`npm run build`)
- [ ] 환경 변수 확인 (`.env.production`)
- [ ] API URL 확인 (Backend 배포 완료)
- [ ] Git 커밋 및 푸시 완료
- [ ] Git 태그 생성 (버전 관리)

---

### Deployment Checklist

- [ ] S3 업로드 성공
- [ ] CloudFront 캐시 무효화 완료
- [ ] CloudFront URL 접속 확인
- [ ] 로그인 기능 테스트
- [ ] 메뉴 조회 기능 테스트
- [ ] 장바구니 기능 테스트
- [ ] 주문 기능 테스트
- [ ] 주문 내역 조회 테스트
- [ ] 모바일 반응형 확인
- [ ] 브라우저 호환성 확인 (Chrome, Safari, Firefox)

---

### Post-Deployment Checklist

- [ ] CloudWatch 메트릭 확인 (요청 수, 에러율)
- [ ] 사용자 피드백 수집
- [ ] 에러 로그 확인 (Browser Console)
- [ ] 성능 메트릭 확인 (Lighthouse)
- [ ] 배포 문서 업데이트

---

## 5. Deployment Diagram

### Manual Deployment Flow

```
┌─────────────────────────────────────────────────────────┐
│                  Developer                               │
│                                                          │
│  1. npm run build                                        │
│  2. aws s3 sync dist/ s3://bucket --delete               │
│  3. aws cloudfront create-invalidation                   │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   S3 Bucket          │
              │  (Static Files)      │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   CloudFront         │
              │  (CDN, HTTPS)        │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   End Users          │
              └──────────────────────┘
```

---

### CI/CD Deployment Flow

```
┌─────────────────────────────────────────────────────────┐
│                  Developer                               │
│                                                          │
│  1. git commit -m "..."                                  │
│  2. git push origin main                                 │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   GitHub             │
              │  (Code Repository)   │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   GitHub Actions     │
              │  (CI/CD Pipeline)    │
              │  - npm ci            │
              │  - npm run test      │
              │  - npm run build     │
              │  - aws s3 sync       │
              │  - cloudfront inv.   │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   S3 Bucket          │
              │  (Static Files)      │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   CloudFront         │
              │  (CDN, HTTPS)        │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   End Users          │
              └──────────────────────┘
```

---

## 6. Deployment Timeline

### Initial Setup (최초 1회)

| 단계 | 작업 | 소요 시간 |
|------|------|----------|
| 1 | AWS 계정 생성 | 10분 |
| 2 | S3 버킷 생성 | 5분 |
| 3 | CloudFront Distribution 생성 | 10분 |
| 4 | CloudFront 배포 완료 대기 | 10-15분 |
| 5 | AWS CLI 설정 | 5분 |
| **총계** | | **40-45분** |

---

### Regular Deployment (일반 배포)

| 단계 | 작업 | 소요 시간 |
|------|------|----------|
| 1 | 로컬 빌드 (`npm run build`) | 30초 |
| 2 | S3 업로드 (`aws s3 sync`) | 10-30초 |
| 3 | CloudFront 무효화 | 1-5분 |
| 4 | 배포 확인 | 2분 |
| **총계** | | **4-8분** |

---

### CI/CD Deployment (자동 배포)

| 단계 | 작업 | 소요 시간 |
|------|------|----------|
| 1 | GitHub Actions 트리거 | 즉시 |
| 2 | 의존성 설치 (`npm ci`) | 30초 |
| 3 | 테스트 실행 (`npm run test`) | 10초 |
| 4 | 빌드 (`npm run build`) | 30초 |
| 5 | S3 업로드 | 10-30초 |
| 6 | CloudFront 무효화 | 1-5분 |
| **총계** | | **3-7분** |

---

## 7. Deployment Best Practices

### 7.1 Version Tagging

**Git 태그 사용**:
```bash
# 버전 태그 생성
git tag -a v1.0.0 -m "Release version 1.0.0"

# 태그 푸시
git push origin v1.0.0
```

**태그 네이밍 규칙**:
- `v1.0.0` - Major.Minor.Patch (Semantic Versioning)
- `v1.0.0-beta` - 베타 버전
- `v1.0.0-rc1` - Release Candidate

---

### 7.2 Environment Variables

**보안 규칙**:
- `.env` 파일은 Git에 커밋하지 않음 (`.gitignore`에 추가)
- `.env.example` 파일로 템플릿 제공
- GitHub Secrets로 민감한 정보 관리

**예시** (`.env.example`):
```env
VITE_API_URL=https://api.example.com
VITE_ENV=production
```

---

### 7.3 Cache Busting

**Vite 자동 처리**:
- JavaScript/CSS 파일명에 해시 추가 (예: `main.abc123.js`)
- 파일 변경 시 해시 자동 변경
- 브라우저 캐시 무효화 자동 처리

**CloudFront 설정**:
- HTML: 캐시 없음 (`Cache-Control: no-cache`)
- JS/CSS: 1년 캐시 (파일명에 해시 포함)
- Images: 1주일 캐시

---

### 7.4 Monitoring

**CloudWatch 알림 설정** (선택사항):
```bash
# CloudWatch 알림 생성
aws cloudwatch put-metric-alarm \
  --alarm-name customer-frontend-error-rate \
  --alarm-description "Alert when error rate > 5%" \
  --metric-name 4xxErrorRate \
  --namespace AWS/CloudFront \
  --statistic Average \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1
```

---

### 7.5 Backup

**S3 Versioning**:
- 모든 파일 변경 이력 보관
- 실수로 삭제 시 복구 가능
- 추가 비용 미미 (변경된 파일만 저장)

**Git Repository**:
- 소스 코드는 Git으로 관리
- GitHub에 백업
- 언제든지 재빌드 가능

---

## 8. Troubleshooting

### Issue 1: CloudFront에서 404 에러

**원인**: SPA 라우팅 설정 누락

**해결**:
```bash
# CloudFront Error Pages 설정
# 404 → /index.html (200 응답)
# 403 → /index.html (200 응답)
```

---

### Issue 2: 캐시가 업데이트되지 않음

**원인**: CloudFront 캐시 무효화 누락

**해결**:
```bash
# 캐시 무효화
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"
```

---

### Issue 3: API 호출 실패 (CORS 에러)

**원인**: Backend CORS 설정 누락

**해결**:
```python
# Backend (FastAPI)
origins = [
    "https://d1234567890abc.cloudfront.net",
    "http://localhost:5173"  # 개발 환경
]
```

---

### Issue 4: 환경 변수가 적용되지 않음

**원인**: 빌드 시 환경 변수 누락

**해결**:
```bash
# 환경 변수 확인
cat .env.production

# 빌드 시 환경 변수 명시
VITE_API_URL=https://api.example.com npm run build
```

---

## Deployment Summary

| 항목 | 초기 설정 | 일반 배포 | CI/CD 배포 |
|------|----------|----------|-----------|
| 소요 시간 | 40-45분 | 4-8분 | 3-7분 |
| 수동 작업 | 많음 | 중간 | 없음 |
| 에러 가능성 | 높음 | 중간 | 낮음 |
| 권장 시기 | 최초 1회 | 초기 개발 | 프로덕션 |

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
