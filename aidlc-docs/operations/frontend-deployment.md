# Frontend Deployment Guide

## Overview

Customer Frontend와 Admin Frontend를 AWS S3 + CloudFront에 배포하는 가이드입니다.

**소요 시간**: 각 30-45분 (총 1-1.5시간)  
**예상 비용**: $2/월 (두 Frontend 합계)

---

## Prerequisites

- Backend Service 배포 완료
- Backend API URL 확인 (예: `http://ec2-xx-xx-xx-xx.ap-northeast-2.compute.amazonaws.com`)
- AWS CLI 설정 완료
- Node.js 20+ 설치

---

## Part 1: Customer Frontend Deployment

### Step 1: S3 Bucket 생성

```bash
# S3 버킷 생성
aws s3 mb s3://tableorder-customer-frontend-prod --region ap-northeast-2

# Versioning 활성화 (롤백 지원)
aws s3api put-bucket-versioning \
  --bucket tableorder-customer-frontend-prod \
  --versioning-configuration Status=Enabled
```

### Step 2: CloudFront Distribution 생성

```bash
# Origin Access Identity 생성
aws cloudfront create-cloud-front-origin-access-identity \
  --cloud-front-origin-access-identity-config \
  CallerReference=tableorder-customer-$(date +%s),Comment=TableOrder-Customer-OAI

# OAI ID 기록 (예: E1234567890ABC)
```

**AWS Console에서 CloudFront Distribution 생성**:
1. AWS Console → CloudFront → Create Distribution
2. 설정:
   - Origin Domain: `tableorder-customer-frontend-prod.s3.ap-northeast-2.amazonaws.com`
   - Origin Access: Origin Access Identity → 위에서 생성한 OAI 선택
   - Viewer Protocol Policy: Redirect HTTP to HTTPS
   - Allowed HTTP Methods: GET, HEAD
   - Cache Policy: CachingOptimized
   - Default Root Object: `index.html`
   - Error Pages:
     - 404 → `/index.html` (200 응답)
     - 403 → `/index.html` (200 응답)

3. Create Distribution 클릭
4. 배포 완료 대기 (약 10-15분)

### Step 3: S3 Bucket Policy 설정

```bash
# Bucket Policy 설정 (CloudFront에서만 접근 허용)
aws s3api put-bucket-policy \
  --bucket tableorder-customer-frontend-prod \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "AllowCloudFrontAccess",
        "Effect": "Allow",
        "Principal": {
          "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity {OAI-ID}"
        },
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::tableorder-customer-frontend-prod/*"
      }
    ]
  }'
```

**중요**: `{OAI-ID}`를 실제 OAI ID로 교체하세요!

### Step 4: 로컬 빌드

```bash
cd customer-frontend

# 환경 변수 설정
cat > .env.production <<EOF
VITE_API_URL=http://{ec2-public-ip}
VITE_ENV=production
EOF

# 의존성 설치
npm install

# 프로덕션 빌드
npm run build

# 빌드 결과물 확인
ls -la dist/
```

### Step 5: S3 업로드

```bash
# S3에 업로드
aws s3 sync dist/ s3://tableorder-customer-frontend-prod --delete

# 업로드 확인
aws s3 ls s3://tableorder-customer-frontend-prod/
```

### Step 6: CloudFront 캐시 무효화

```bash
# Distribution ID 확인
aws cloudfront list-distributions \
  --query "DistributionList.Items[?Origins.Items[0].DomainName=='tableorder-customer-frontend-prod.s3.ap-northeast-2.amazonaws.com'].Id" \
  --output text

# 캐시 무효화
aws cloudfront create-invalidation \
  --distribution-id {distribution-id} \
  --paths "/*"
```

### Step 7: 배포 확인

```bash
# CloudFront URL 확인
aws cloudfront list-distributions \
  --query "DistributionList.Items[?Origins.Items[0].DomainName=='tableorder-customer-frontend-prod.s3.ap-northeast-2.amazonaws.com'].DomainName" \
  --output text

# 브라우저에서 접속
# https://d1234567890abc.cloudfront.net
```

**테스트**:
- 로그인 페이지 로드 확인
- 테이블 로그인 테스트
- 메뉴 조회 테스트
- 장바구니 추가 테스트
- 주문 생성 테스트

---

## Part 2: Admin Frontend Deployment

### Step 1: S3 Bucket 생성

```bash
# S3 버킷 생성
aws s3 mb s3://tableorder-admin-frontend-prod --region ap-northeast-2

# Versioning 활성화
aws s3api put-bucket-versioning \
  --bucket tableorder-admin-frontend-prod \
  --versioning-configuration Status=Enabled
```

### Step 2: CloudFront Distribution 생성

**AWS Console에서 CloudFront Distribution 생성** (Customer Frontend와 동일한 과정):
1. AWS Console → CloudFront → Create Distribution
2. 설정:
   - Origin Domain: `tableorder-admin-frontend-prod.s3.ap-northeast-2.amazonaws.com`
   - Origin Access: 새 OAI 생성 또는 기존 OAI 재사용
   - Viewer Protocol Policy: Redirect HTTP to HTTPS
   - Default Root Object: `index.html`
   - Error Pages: 404, 403 → `/index.html` (200 응답)

3. Create Distribution 클릭
4. 배포 완료 대기 (약 10-15분)

### Step 3: S3 Bucket Policy 설정

```bash
# Bucket Policy 설정
aws s3api put-bucket-policy \
  --bucket tableorder-admin-frontend-prod \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "AllowCloudFrontAccess",
        "Effect": "Allow",
        "Principal": {
          "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity {OAI-ID}"
        },
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::tableorder-admin-frontend-prod/*"
      }
    ]
  }'
```

### Step 4: Admin Frontend 구현 완료 (필요 시)

**Admin Frontend는 핵심 파일만 생성되었으므로, 나머지 파일 구현 필요**:

```bash
cd admin-frontend

# Customer Frontend에서 공통 파일 복사
cp -r ../customer-frontend/src/components/shared ./src/components/
cp ../customer-frontend/src/assets/main.css ./src/assets/
cp ../customer-frontend/tailwind.config.js ./
cp ../customer-frontend/postcss.config.js ./
cp ../customer-frontend/.eslintrc.js ./
cp ../customer-frontend/.gitignore ./

# 나머지 파일 구현 (README.md 참조)
# - src/services/api.js
# - src/services/sse.js
# - src/stores/order.js, table.js, menu.js, toast.js
# - src/views/ (4개 Views)
# - src/components/ (TableCard, OrderList, MenuForm 등)
```

**예상 시간**: 2시간 (Customer Frontend 패턴 재사용)

### Step 5: 로컬 빌드

```bash
cd admin-frontend

# 환경 변수 설정
cat > .env.production <<EOF
VITE_API_URL=http://{ec2-public-ip}
VITE_ENV=production
EOF

# 의존성 설치
npm install

# 프로덕션 빌드
npm run build

# 빌드 결과물 확인
ls -la dist/
```

### Step 6: S3 업로드

```bash
# S3에 업로드
aws s3 sync dist/ s3://tableorder-admin-frontend-prod --delete

# 업로드 확인
aws s3 ls s3://tableorder-admin-frontend-prod/
```

### Step 7: CloudFront 캐시 무효화

```bash
# Distribution ID 확인
aws cloudfront list-distributions \
  --query "DistributionList.Items[?Origins.Items[0].DomainName=='tableorder-admin-frontend-prod.s3.ap-northeast-2.amazonaws.com'].Id" \
  --output text

# 캐시 무효화
aws cloudfront create-invalidation \
  --distribution-id {distribution-id} \
  --paths "/*"
```

### Step 8: 배포 확인

```bash
# CloudFront URL 확인
aws cloudfront list-distributions \
  --query "DistributionList.Items[?Origins.Items[0].DomainName=='tableorder-admin-frontend-prod.s3.ap-northeast-2.amazonaws.com'].DomainName" \
  --output text

# 브라우저에서 접속
# https://d9876543210xyz.cloudfront.net
```

**테스트**:
- 로그인 페이지 로드 확인
- 관리자 로그인 테스트
- 주문 대시보드 로드 확인
- SSE 실시간 업데이트 테스트
- 테이블 관리 테스트
- 메뉴 관리 테스트

---

## Continuous Deployment (향후)

### GitHub Actions 워크플로우

**Customer Frontend** (`.github/workflows/deploy-customer.yml`):
```yaml
name: Deploy Customer Frontend

on:
  push:
    branches: [main]
    paths:
      - 'customer-frontend/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - name: Install and Build
        working-directory: customer-frontend
        run: |
          npm ci
          npm run build
        env:
          VITE_API_URL: ${{ secrets.VITE_API_URL }}
      - name: Deploy to S3
        run: |
          aws s3 sync customer-frontend/dist/ s3://tableorder-customer-frontend-prod --delete
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      - name: Invalidate CloudFront
        run: |
          aws cloudfront create-invalidation --distribution-id ${{ secrets.CF_CUSTOMER_DIST_ID }} --paths "/*"
```

**Admin Frontend** (`.github/workflows/deploy-admin.yml`):
```yaml
name: Deploy Admin Frontend

on:
  push:
    branches: [main]
    paths:
      - 'admin-frontend/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - name: Install and Build
        working-directory: admin-frontend
        run: |
          npm ci
          npm run build
        env:
          VITE_API_URL: ${{ secrets.VITE_API_URL }}
      - name: Deploy to S3
        run: |
          aws s3 sync admin-frontend/dist/ s3://tableorder-admin-frontend-prod --delete
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      - name: Invalidate CloudFront
        run: |
          aws cloudfront create-invalidation --distribution-id ${{ secrets.CF_ADMIN_DIST_ID }} --paths "/*"
```

---

## Rollback Procedures

### S3 Versioning을 이용한 롤백

```bash
# 1. 이전 버전 확인
aws s3api list-object-versions \
  --bucket tableorder-customer-frontend-prod \
  --prefix index.html

# 2. 이전 버전 복원
aws s3api copy-object \
  --copy-source "tableorder-customer-frontend-prod/index.html?versionId={version-id}" \
  --bucket tableorder-customer-frontend-prod \
  --key index.html

# 3. CloudFront 캐시 무효화
aws cloudfront create-invalidation \
  --distribution-id {distribution-id} \
  --paths "/*"
```

### Git 태그를 이용한 롤백

```bash
# 1. 이전 버전 체크아웃
git checkout v1.0.0

# 2. 재빌드
cd customer-frontend
npm run build

# 3. 재배포
aws s3 sync dist/ s3://tableorder-customer-frontend-prod --delete
aws cloudfront create-invalidation --distribution-id {distribution-id} --paths "/*"

# 4. 원래 브랜치로 복귀
git checkout main
```

---

## Troubleshooting

### Issue 1: CloudFront에서 404 에러

**원인**: SPA 라우팅 설정 누락

**해결**: CloudFront Error Pages 설정 확인
- 404 → `/index.html` (200 응답)
- 403 → `/index.html` (200 응답)

### Issue 2: API 호출 실패 (CORS 에러)

**원인**: Backend CORS 설정 누락

**해결**: Backend `.env` 파일에 Frontend URL 추가
```bash
FRONTEND_URL=https://d1234567890abc.cloudfront.net,https://d9876543210xyz.cloudfront.net
```

Backend 재시작:
```bash
sudo systemctl restart tableorder
```

### Issue 3: 캐시가 업데이트되지 않음

**원인**: CloudFront 캐시 무효화 누락

**해결**:
```bash
aws cloudfront create-invalidation \
  --distribution-id {distribution-id} \
  --paths "/*"
```

---

## Post-Deployment Checklist

### Customer Frontend
- [ ] S3 버킷 생성 완료
- [ ] CloudFront Distribution 생성 완료
- [ ] 빌드 성공
- [ ] S3 업로드 완료
- [ ] CloudFront 캐시 무효화 완료
- [ ] 로그인 페이지 로드 확인
- [ ] 테이블 로그인 테스트 통과
- [ ] 메뉴 조회 테스트 통과
- [ ] 장바구니 기능 테스트 통과
- [ ] 주문 생성 테스트 통과

### Admin Frontend
- [ ] S3 버킷 생성 완료
- [ ] CloudFront Distribution 생성 완료
- [ ] 나머지 파일 구현 완료 (필요 시)
- [ ] 빌드 성공
- [ ] S3 업로드 완료
- [ ] CloudFront 캐시 무효화 완료
- [ ] 로그인 페이지 로드 확인
- [ ] 관리자 로그인 테스트 통과
- [ ] 주문 대시보드 로드 확인
- [ ] SSE 실시간 업데이트 테스트 통과
- [ ] 테이블 관리 테스트 통과
- [ ] 메뉴 관리 테스트 통과

---

## Next Steps

1. **통합 테스트**: 전체 시스템 통합 테스트
2. **성능 테스트**: Lighthouse 성능 측정
3. **보안 테스트**: XSS, CSRF 방어 확인
4. **모니터링 설정**: CloudWatch Alarms 설정
5. **커스텀 도메인 설정** (선택사항): Route 53 + ACM 인증서

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
