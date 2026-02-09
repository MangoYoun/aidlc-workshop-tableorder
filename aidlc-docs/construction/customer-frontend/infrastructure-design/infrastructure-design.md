# Infrastructure Design - Customer Frontend

## Overview

Customer Frontend의 인프라 설계를 정의합니다. Vue.js SPA를 위한 정적 호스팅 및 배포 인프라를 명시합니다.

---

## 1. Deployment Environment

### 선택: AWS S3 + CloudFront

**이유**:
- **정적 호스팅**: Vue.js 빌드 결과물은 정적 파일 (HTML, CSS, JS)
- **비용 효율**: 서버 불필요, 트래픽 기반 과금
- **확장성**: CloudFront CDN으로 전 세계 배포
- **간단한 설정**: S3 버킷 + CloudFront 배포만으로 완료

**대안**:
- Netlify/Vercel: 더 간단하지만 AWS 생태계 통합 약함
- EC2 + Nginx: 과도한 복잡도, 정적 파일에 불필요
- Amplify Hosting: AWS 통합 우수하지만 추가 비용

---

## 2. Infrastructure Components

### Component 2.1: S3 Bucket (정적 파일 저장)

**서비스**: AWS S3  
**용도**: 빌드된 정적 파일 저장 및 호스팅

**설정**:
```
Bucket Name: tableorder-customer-frontend
Region: ap-northeast-2 (서울)
Versioning: Enabled (롤백 지원)
Public Access: Blocked (CloudFront를 통해서만 접근)
```

**저장 파일**:
- `index.html` - SPA 진입점
- `assets/` - JS, CSS 번들
- `images/` - 이미지 파일

**예상 용량**: 10-20MB (빌드 결과물)

---

### Component 2.2: CloudFront Distribution (CDN)

**서비스**: AWS CloudFront  
**용도**: 전 세계 사용자에게 빠른 콘텐츠 전송

**설정**:
```
Origin: S3 Bucket (tableorder-customer-frontend)
Price Class: Use Only North America, Europe, Asia (저렴한 옵션)
Default Root Object: index.html
Error Pages: 
  - 404 → /index.html (SPA 라우팅 지원)
  - 403 → /index.html
HTTPS: Required (Redirect HTTP to HTTPS)
Caching: 
  - HTML: No cache (항상 최신)
  - JS/CSS: 1년 (파일명에 해시 포함)
  - Images: 1주일
```

**장점**:
- 빠른 로딩 속도 (엣지 로케이션 캐싱)
- HTTPS 자동 지원
- DDoS 방어

---

### Component 2.3: Route 53 (DNS - 선택사항)

**서비스**: AWS Route 53  
**용도**: 도메인 이름 관리 (선택사항)

**설정**:
```
Domain: tableorder.example.com (예시)
Record Type: A (Alias to CloudFront)
```

**참고**: 개발/테스트 환경에서는 CloudFront URL 직접 사용 가능

---

## 3. Infrastructure Mapping

### Logical Component → Infrastructure Service

| 논리적 컴포넌트 | AWS 서비스 | 용도 |
|----------------|-----------|------|
| Static Files | S3 Bucket | HTML, JS, CSS, Images 저장 |
| CDN | CloudFront | 전 세계 콘텐츠 전송 |
| DNS | Route 53 | 도메인 이름 (선택사항) |
| SSL/TLS | CloudFront | HTTPS 지원 |

---

## 4. Environment Configuration

### 4.1 Development Environment

**배포 대상**: 개발자 로컬 또는 개발 S3 버킷

**설정**:
```
S3 Bucket: tableorder-customer-frontend-dev
CloudFront: 별도 Distribution (선택사항)
API URL: http://localhost:8000 (로컬 Backend)
```

**환경 변수** (`.env.development`):
```env
VITE_API_URL=http://localhost:8000
VITE_ENV=development
```

---

### 4.2 Production Environment

**배포 대상**: 프로덕션 S3 버킷 + CloudFront

**설정**:
```
S3 Bucket: tableorder-customer-frontend-prod
CloudFront: 프로덕션 Distribution
API URL: https://api.tableorder.example.com (프로덕션 Backend)
```

**환경 변수** (`.env.production`):
```env
VITE_API_URL=https://api.tableorder.example.com
VITE_ENV=production
```

---

## 5. Deployment Pipeline

### 5.1 Manual Deployment (초기)

**단계**:
1. 로컬에서 빌드
   ```bash
   npm run build
   ```

2. S3에 업로드
   ```bash
   aws s3 sync dist/ s3://tableorder-customer-frontend-prod --delete
   ```

3. CloudFront 캐시 무효화
   ```bash
   aws cloudfront create-invalidation --distribution-id E1234567890ABC --paths "/*"
   ```

**장점**: 간단한 구현  
**단점**: 수동 작업 필요

---

### 5.2 CI/CD Pipeline (향후)

**도구**: GitHub Actions 또는 AWS CodePipeline

**단계**:
1. 코드 푸시 (GitHub)
2. 자동 빌드 (GitHub Actions)
3. S3 업로드
4. CloudFront 무효화
5. 배포 완료 알림

**예시** (GitHub Actions):
```yaml
name: Deploy to S3
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: npm install
      - name: Build
        run: npm run build
      - name: Deploy to S3
        run: aws s3 sync dist/ s3://tableorder-customer-frontend-prod --delete
      - name: Invalidate CloudFront
        run: aws cloudfront create-invalidation --distribution-id ${{ secrets.CF_DISTRIBUTION_ID }} --paths "/*"
```

---

## 6. Cost Estimation

### Monthly Cost (예상)

| 서비스 | 사용량 | 비용 (USD) |
|--------|--------|-----------|
| S3 Storage | 20MB | $0.01 |
| S3 Requests | 10,000 GET | $0.01 |
| CloudFront Data Transfer | 10GB | $0.85 |
| CloudFront Requests | 100,000 | $0.10 |
| Route 53 (선택) | 1 Hosted Zone | $0.50 |
| **총계** | | **$1.47 ~ $1.97/월** |

**참고**: 
- 매우 저렴한 비용
- 트래픽 증가 시 CloudFront 비용만 증가
- 서버 비용 없음

---

## 7. Scalability

### 7.1 Horizontal Scalability

**자동 확장**: CloudFront가 자동으로 처리
- 트래픽 증가 시 엣지 로케이션 자동 확장
- 무제한 동시 사용자 지원

**제약 없음**: 정적 파일이므로 Backend 확장성에만 의존

---

### 7.2 Geographic Distribution

**CloudFront 엣지 로케이션**:
- 한국: 서울
- 아시아: 도쿄, 싱가포르, 홍콩
- 전 세계: 200+ 엣지 로케이션

**장점**: 전 세계 어디서나 빠른 로딩

---

## 8. Security

### 8.1 HTTPS

**CloudFront**: 자동 HTTPS 지원
- AWS Certificate Manager (ACM)로 무료 SSL 인증서
- HTTP → HTTPS 자동 리다이렉트

---

### 8.2 S3 Bucket Security

**Public Access**: Blocked
- CloudFront를 통해서만 접근 가능
- Origin Access Identity (OAI) 사용

**Bucket Policy**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCloudFrontAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E1234567890ABC"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::tableorder-customer-frontend-prod/*"
    }
  ]
}
```

---

### 8.3 CORS Configuration

**S3 CORS**: 불필요 (CloudFront가 처리)

**Backend CORS**: Backend에서 Frontend URL 허용
```python
# Backend (FastAPI)
origins = [
    "https://d1234567890abc.cloudfront.net",  # CloudFront URL
    "https://tableorder.example.com"  # Custom Domain
]
```

---

## 9. Monitoring

### 9.1 CloudFront Metrics

**CloudWatch 메트릭**:
- Requests: 요청 수
- BytesDownloaded: 다운로드 용량
- ErrorRate: 4xx/5xx 에러율

**알림 설정** (선택사항):
- ErrorRate > 5%: 알림

---

### 9.2 S3 Metrics

**CloudWatch 메트릭**:
- BucketSizeBytes: 버킷 크기
- NumberOfObjects: 객체 수

**참고**: 정적 파일이므로 모니터링 최소화

---

## 10. Backup and Recovery

### 10.1 S3 Versioning

**설정**: Enabled
- 파일 변경 이력 보관
- 실수로 삭제 시 복구 가능

---

### 10.2 Rollback Strategy

**방법 1**: S3 버전 복원
```bash
aws s3api list-object-versions --bucket tableorder-customer-frontend-prod
aws s3api copy-object --copy-source "bucket/key?versionId=xxx" --bucket bucket --key key
```

**방법 2**: Git 태그 + 재배포
```bash
git checkout v1.0.0
npm run build
aws s3 sync dist/ s3://tableorder-customer-frontend-prod --delete
```

---

## Infrastructure Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                      Internet                            │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Route 53 (DNS)     │ (선택사항)
              │  tableorder.com      │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   CloudFront (CDN)   │
              │  - HTTPS             │
              │  - Caching           │
              │  - Global Edge       │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   S3 Bucket          │
              │  - Static Files      │
              │  - Versioning        │
              │  - Private Access    │
              └──────────────────────┘
```

---

## Infrastructure Summary

| 항목 | 선택 | 이유 |
|------|------|------|
| 호스팅 | S3 + CloudFront | 정적 파일, 비용 효율, 확장성 |
| CDN | CloudFront | 빠른 로딩, HTTPS, 전 세계 배포 |
| DNS | Route 53 (선택) | AWS 통합, 간단한 설정 |
| 배포 | Manual → CI/CD | 초기 수동, 향후 자동화 |
| 비용 | ~$2/월 | 매우 저렴 |
| 확장성 | 무제한 | CloudFront 자동 확장 |
| 보안 | HTTPS, OAI | 안전한 접근 제어 |

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
