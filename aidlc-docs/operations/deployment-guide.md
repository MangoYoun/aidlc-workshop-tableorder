# Deployment Guide - TableOrder Service

## Overview

테이블오더 서비스의 전체 배포 가이드입니다. 3개 Unit (Backend Service, Customer Frontend, Admin Frontend)을 AWS에 배포하는 과정을 단계별로 설명합니다.

**배포 대상**:
- Unit 1: Backend Service (AWS EC2 + RDS)
- Unit 2: Customer Frontend (AWS S3 + CloudFront)
- Unit 3: Admin Frontend (AWS S3 + CloudFront)

**예상 소요 시간**: 2-3시간 (최초 배포)

**예상 월간 비용**: $56-67 (Backend $54-65 + Frontend $2)

---

## Prerequisites

### 1. AWS 계정
- AWS 계정 생성 완료
- IAM 사용자 생성 (AdministratorAccess 권한)
- Access Key ID 및 Secret Access Key 발급

### 2. 로컬 환경
- AWS CLI 설치 및 설정
- Node.js 20+ 설치
- Python 3.9+ 설치
- Git 설치

### 3. 도메인 (선택사항)
- 커스텀 도메인 (예: tableorder.example.com)
- Route 53 또는 외부 DNS 제공자

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Internet                             │
└────────────────────────────┬────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
    ┌───────────────────┐     ┌───────────────────┐
    │  CloudFront (CDN) │     │  CloudFront (CDN) │
    │  Customer Frontend│     │  Admin Frontend   │
    └─────────┬─────────┘     └─────────┬─────────┘
              │                         │
              ▼                         ▼
    ┌───────────────────┐     ┌───────────────────┐
    │  S3 Bucket        │     │  S3 Bucket        │
    │  (Static Files)   │     │  (Static Files)   │
    └───────────────────┘     └───────────────────┘
                             │
                             ▼
              ┌──────────────────────────┐
              │   EC2 Instance           │
              │   (Backend Service)      │
              └──────────┬───────────────┘
                         │
                         ▼
              ┌──────────────────────────┐
              │   RDS PostgreSQL         │
              │   (Database)             │
              └──────────────────────────┘
```

---

## Deployment Sequence

**권장 순서**:
1. Backend Service 배포 (EC2 + RDS)
2. Customer Frontend 배포 (S3 + CloudFront)
3. Admin Frontend 배포 (S3 + CloudFront)
4. 통합 테스트 및 검증

**이유**: Frontend는 Backend API에 의존하므로 Backend를 먼저 배포해야 합니다.

---

## Part 1: Backend Service Deployment

상세 내용은 `backend-deployment.md` 참조

**요약**:
1. RDS PostgreSQL 생성 (db.t3.small)
2. EC2 인스턴스 생성 (t3.small)
3. FastAPI 애플리케이션 배포
4. Database 스키마 마이그레이션
5. Systemd 서비스 설정
6. Nginx 리버스 프록시 설정
7. CloudWatch Logs 설정

**소요 시간**: 1-1.5시간

**결과**: Backend API 엔드포인트 (예: `http://ec2-xx-xx-xx-xx.ap-northeast-2.compute.amazonaws.com`)

---

## Part 2: Customer Frontend Deployment

상세 내용은 `frontend-deployment.md` 참조

**요약**:
1. S3 버킷 생성
2. CloudFront Distribution 생성
3. 로컬 빌드 (`npm run build`)
4. S3 업로드 (`aws s3 sync`)
5. CloudFront 캐시 무효화

**소요 시간**: 30-45분

**결과**: Customer Frontend URL (예: `https://d1234567890abc.cloudfront.net`)

---

## Part 3: Admin Frontend Deployment

상세 내용은 `frontend-deployment.md` 참조

**요약**:
1. S3 버킷 생성
2. CloudFront Distribution 생성
3. 로컬 빌드 (`npm run build`)
4. S3 업로드 (`aws s3 sync`)
5. CloudFront 캐시 무효화

**소요 시간**: 30-45분

**결과**: Admin Frontend URL (예: `https://d9876543210xyz.cloudfront.net`)

---

## Part 4: Integration Testing

**테스트 시나리오**:
1. Customer Frontend → Backend API 통합
   - 테이블 로그인
   - 메뉴 조회
   - 장바구니 추가
   - 주문 생성
   - 주문 내역 조회

2. Admin Frontend → Backend API 통합
   - 관리자 로그인
   - 실시간 주문 모니터링 (SSE)
   - 주문 상태 변경
   - 테이블 관리
   - 메뉴 관리

**소요 시간**: 30분

---

## Post-Deployment Checklist

- [ ] Backend API Health Check 확인 (`/health`)
- [ ] Customer Frontend 접속 확인
- [ ] Admin Frontend 접속 확인
- [ ] 테이블 로그인 테스트
- [ ] 관리자 로그인 테스트
- [ ] 주문 생성 테스트
- [ ] SSE 실시간 업데이트 테스트
- [ ] CloudWatch Logs 확인
- [ ] CloudWatch Alarms 설정
- [ ] 비용 모니터링 설정

---

## Monitoring and Maintenance

### CloudWatch Dashboards

**Backend Metrics**:
- EC2 CPU Utilization
- RDS Database Connections
- API Response Time
- Error Rate

**Frontend Metrics**:
- CloudFront Requests
- CloudFront Error Rate
- S3 Storage Size

### Alarms

**Critical Alarms**:
- Backend CPU > 80%
- RDS Connections > 10
- API Error Rate > 5%
- CloudFront Error Rate > 5%

### Logs

**Backend Logs**:
- CloudWatch Logs: `/aws/ec2/tableorder-backend`
- Retention: 7일

**Frontend Logs**:
- Browser Console (개발자 도구)
- CloudFront Access Logs (선택사항)

---

## Cost Optimization

### Reserved Instances (1년 약정)
- EC2 t3.small: 30-40% 절감
- RDS db.t3.small: 30-40% 절감

### S3 Lifecycle Policy
- 오래된 이미지를 S3 Glacier로 이동

### CloudWatch Logs Retention
- 7일로 제한하여 비용 절감

**예상 절감**: 월 $15-20

---

## Disaster Recovery

### Backup Strategy

**RDS Automated Backups**:
- 일별 자동 백업 (03:00-04:00)
- 7일 보관
- Point-in-Time Recovery 지원

**S3 Versioning**:
- 모든 파일 변경 이력 보관
- 실수로 삭제 시 복구 가능

**Git Repository**:
- 소스 코드는 Git으로 관리
- 언제든지 재빌드 가능

### Recovery Procedures

**RDS 복구**:
```bash
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier tableorder-db \
  --target-db-instance-identifier tableorder-db-restored \
  --restore-time 2026-02-09T12:00:00Z
```

**Frontend 롤백**:
```bash
# S3 버전 복원
aws s3api list-object-versions --bucket tableorder-customer-frontend-prod
aws s3api copy-object --copy-source "bucket/key?versionId=xxx" --bucket bucket --key key

# CloudFront 캐시 무효화
aws cloudfront create-invalidation --distribution-id E1234567890ABC --paths "/*"
```

---

## Next Steps

1. **배포 문서 읽기**:
   - `backend-deployment.md` - Backend 배포 상세 가이드
   - `frontend-deployment.md` - Frontend 배포 상세 가이드

2. **배포 실행**:
   - Backend Service 배포
   - Customer Frontend 배포
   - Admin Frontend 배포

3. **테스트 및 검증**:
   - 통합 테스트 실행
   - 성능 테스트 실행
   - 보안 테스트 실행

4. **모니터링 설정**:
   - CloudWatch Alarms 설정
   - 로그 모니터링 설정

5. **문서화**:
   - 배포 과정 기록
   - 트러블슈팅 가이드 작성

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
