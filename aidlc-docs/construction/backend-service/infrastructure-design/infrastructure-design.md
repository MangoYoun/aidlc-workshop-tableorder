# Infrastructure Design - Backend Service

## Overview

Backend Service의 논리적 컴포넌트를 AWS 인프라 서비스로 매핑하고, 배포 아키텍처를 정의합니다.

**Target Environment**: 중소규모 매장 3-10개 (동시 사용자 10-50명)  
**Cloud Provider**: AWS (Amazon Web Services)  
**Deployment Strategy**: 단일 리전, 단일 가용 영역 (초기 구성)

---

## 1. Infrastructure Service Mapping

### 1.1 Compute Services

#### Backend Application Server

**Logical Component**: FastAPI Application

**Infrastructure Service**: **AWS EC2 (Elastic Compute Cloud)**

**Instance Specification**:
- **Instance Type**: t3.small
- **vCPU**: 2
- **Memory**: 2GB RAM
- **Storage**: 20GB EBS (gp3)
- **Operating System**: Ubuntu 22.04 LTS

**Rationale**:
- t3.small은 중소규모 애플리케이션에 적합
- 2 vCPU와 2GB RAM으로 FastAPI 서버와 동시 사용자 10-50명 처리 가능
- Burstable 성능으로 트래픽 변동에 대응
- 비용 효율적 (월 약 $15-20)

**Configuration**:
```bash
# EC2 User Data (초기 설정 스크립트)
#!/bin/bash
apt-get update
apt-get install -y python3.9 python3-pip git
pip3 install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib python-dotenv
```

---

### 1.2 Database Services

#### PostgreSQL Database

**Logical Component**: PostgreSQL Database

**Infrastructure Service**: **AWS RDS (Relational Database Service) - PostgreSQL**

**Instance Specification**:
- **Instance Type**: db.t3.small
- **vCPU**: 2
- **Memory**: 2GB RAM
- **Storage**: 20GB SSD (gp3)
- **Engine Version**: PostgreSQL 14.x
- **Multi-AZ**: No (단일 가용 영역)
- **Backup Retention**: 7일

**Rationale**:
- db.t3.small은 중소규모 데이터베이스에 적합
- 2 vCPU와 2GB RAM으로 동시 연결 10-15개 처리 가능
- RDS 관리형 서비스로 자동 백업, 패치, 모니터링 제공
- 비용 효율적 (월 약 $25-30)

**Configuration**:
```yaml
# RDS Configuration
Engine: postgres
EngineVersion: 14.x
DBInstanceClass: db.t3.small
AllocatedStorage: 20
StorageType: gp3
BackupRetentionPeriod: 7
PreferredBackupWindow: "03:00-04:00"
PreferredMaintenanceWindow: "sun:04:00-sun:05:00"
PubliclyAccessible: false
```

---

### 1.3 Storage Services

#### Application Logs

**Logical Component**: Logging System

**Infrastructure Service**: **AWS CloudWatch Logs**

**Configuration**:
- **Log Group**: `/aws/ec2/tableorder-backend`
- **Retention**: 7일
- **Log Streams**: 인스턴스별 자동 생성

**Rationale**:
- EC2 인스턴스 종료 시에도 로그 보존
- 중앙 집중식 로그 관리
- 검색 및 필터링 기능 제공
- 무료 티어에서 일정량까지 무료

**Log Agent Setup**:
```bash
# CloudWatch Logs Agent 설치
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
dpkg -i amazon-cloudwatch-agent.deb

# Agent 설정
cat > /opt/aws/amazon-cloudwatch-agent/etc/config.json <<EOF
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/tableorder/app.log",
            "log_group_name": "/aws/ec2/tableorder-backend",
            "log_stream_name": "{instance_id}"
          }
        ]
      }
    }
  }
}
EOF
```

#### Menu Images

**Logical Component**: Menu Image Storage

**Infrastructure Service**: **AWS S3 (Simple Storage Service)**

**Configuration**:
- **Bucket Name**: `tableorder-menu-images-{account-id}`
- **Storage Class**: S3 Standard
- **Versioning**: Disabled
- **Public Access**: Block all (CloudFront 또는 Signed URL 사용)

**Rationale**:
- 확장 가능한 객체 스토리지
- 이미지 파일 저장에 최적화
- 저렴한 비용 (GB당 $0.023)
- 99.999999999% 내구성

---

### 1.4 Networking Services

#### VPC and Security Groups

**Infrastructure Service**: **AWS VPC (Virtual Private Cloud)**

**Configuration**:
- **VPC**: Default VPC 사용
- **Subnets**: Default Public Subnets
- **Internet Gateway**: Default IGW

**Security Groups**:

**1. Backend EC2 Security Group**:
```yaml
Name: tableorder-backend-sg
Inbound Rules:
  - Port 80 (HTTP): 0.0.0.0/0
  - Port 443 (HTTPS): 0.0.0.0/0
  - Port 22 (SSH): {Your-IP}/32
Outbound Rules:
  - All traffic: 0.0.0.0/0
```

**2. RDS Security Group**:
```yaml
Name: tableorder-rds-sg
Inbound Rules:
  - Port 5432 (PostgreSQL): {Backend-EC2-SG}
Outbound Rules:
  - None (default deny)
```

**Rationale**:
- Default VPC로 초기 설정 간소화
- 보안 그룹으로 네트워크 접근 제어
- RDS는 EC2에서만 접근 가능 (보안 강화)

---

## 2. Monitoring and Observability

### 2.1 CloudWatch Monitoring

**Infrastructure Service**: **AWS CloudWatch**

**Metrics Collected**:

**EC2 Metrics**:
- CPUUtilization
- NetworkIn/NetworkOut
- DiskReadOps/DiskWriteOps
- StatusCheckFailed

**RDS Metrics**:
- CPUUtilization
- DatabaseConnections
- FreeableMemory
- ReadLatency/WriteLatency

**Custom Metrics** (선택사항):
- API Response Time (Timing Middleware에서 전송)
- Active Sessions Count
- Order Creation Rate

**Alarms** (권장):
```yaml
# EC2 CPU 알람
AlarmName: tableorder-backend-high-cpu
MetricName: CPUUtilization
Threshold: 80%
EvaluationPeriods: 2
Period: 300

# RDS Connection 알람
AlarmName: tableorder-rds-high-connections
MetricName: DatabaseConnections
Threshold: 10
EvaluationPeriods: 2
Period: 300
```

---

### 2.2 Health Check

**Infrastructure Service**: EC2 내장 Health Check

**Endpoint**: `GET /health`

**Health Check Configuration**:
```yaml
HealthCheckPath: /health
HealthCheckIntervalSeconds: 30
HealthyThresholdCount: 2
UnhealthyThresholdCount: 3
```

---

## 3. Security Infrastructure

### 3.1 IAM Roles and Policies

**EC2 Instance Role**:
```yaml
RoleName: tableorder-ec2-role
Policies:
  - CloudWatchLogsFullAccess (로그 전송)
  - S3ReadWriteAccess (메뉴 이미지 업로드)
```

**RDS Access**:
- Security Group으로 제어 (IAM 인증 미사용)

---

### 3.2 Secrets Management

**Infrastructure Service**: **Environment Variables (.env 파일)**

**초기 구성**: EC2 인스턴스의 .env 파일 사용

**향후 확장**: AWS Secrets Manager 또는 AWS Systems Manager Parameter Store

**Environment Variables**:
```bash
# Database
DATABASE_URL=postgresql://user:password@{rds-endpoint}:5432/tableorder

# JWT
JWT_SECRET_KEY={strong-random-key}
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=16

# Session
SESSION_EXPIRE_HOURS=16
SESSION_LAST_ORDER_TIMEOUT_HOURS=2

# CORS
ENVIRONMENT=production
FRONTEND_URL=https://your-frontend-domain.com

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/tableorder/app.log

# AWS
AWS_REGION=ap-northeast-2
S3_BUCKET_NAME=tableorder-menu-images-{account-id}
```

---

## 4. Deployment Architecture

### 4.1 Architecture Diagram (Text Format)

```
┌─────────────────────────────────────────────────────────────┐
│                         Internet                             │
└────────────────────────────┬────────────────────────────────┘
                             │
                             │ HTTPS
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                      AWS Cloud                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  Default VPC                           │  │
│  │                                                         │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │         Public Subnet (Default)                  │  │  │
│  │  │                                                   │  │  │
│  │  │  ┌──────────────────────────────────────────┐  │  │  │
│  │  │  │       EC2 Instance (t3.small)            │  │  │  │
│  │  │  │                                           │  │  │  │
│  │  │  │  ┌────────────────────────────────────┐ │  │  │  │
│  │  │  │  │   FastAPI Application              │ │  │  │  │
│  │  │  │  │   - API Endpoints                  │ │  │  │  │
│  │  │  │  │   - Business Logic                 │ │  │  │  │
│  │  │  │  │   - Authentication                 │ │  │  │  │
│  │  │  │  └────────────────────────────────────┘ │  │  │  │
│  │  │  │                                           │  │  │  │
│  │  │  │  ┌────────────────────────────────────┐ │  │  │  │
│  │  │  │  │   CloudWatch Logs Agent            │ │  │  │  │
│  │  │  │  └────────────────────────────────────┘ │  │  │  │
│  │  │  └──────────────────────────────────────────┘  │  │  │
│  │  │                      │                          │  │  │
│  │  │                      │ PostgreSQL Protocol      │  │  │
│  │  │                      ↓                          │  │  │
│  │  │  ┌──────────────────────────────────────────┐  │  │  │
│  │  │  │   RDS PostgreSQL (db.t3.small)           │  │  │  │
│  │  │  │   - 8 Tables                             │  │  │  │
│  │  │  │   - Auto Backup (7 days)                 │  │  │  │
│  │  │  └──────────────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              CloudWatch Logs                           │  │
│  │              - Log Group: /aws/ec2/tableorder-backend │  │
│  │              - Retention: 7 days                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              S3 Bucket                                 │  │
│  │              - Menu Images                             │  │
│  │              - Private Access                          │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              CloudWatch Monitoring                     │  │
│  │              - EC2 Metrics                             │  │
│  │              - RDS Metrics                             │  │
│  │              - Custom Metrics                          │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

### 4.2 Network Flow

**1. Client → Backend API**:
```
Client (Browser) 
  → Internet 
  → EC2 Public IP (Port 80/443) 
  → FastAPI Application
```

**2. Backend → Database**:
```
FastAPI Application 
  → RDS Security Group (Port 5432) 
  → RDS PostgreSQL
```

**3. Backend → CloudWatch Logs**:
```
FastAPI Application 
  → Log File (/var/log/tableorder/app.log) 
  → CloudWatch Logs Agent 
  → CloudWatch Logs
```

**4. Backend → S3 (Menu Images)**:
```
FastAPI Application 
  → S3 API 
  → S3 Bucket (tableorder-menu-images)
```

---

## 5. Cost Estimation

### 5.1 Monthly Cost Breakdown

| Service | Specification | Monthly Cost (USD) |
|---------|---------------|-------------------|
| EC2 (t3.small) | 2 vCPU, 2GB RAM | $15-20 |
| RDS (db.t3.small) | 2 vCPU, 2GB RAM, 20GB | $25-30 |
| EBS (EC2 Storage) | 20GB gp3 | $2 |
| CloudWatch Logs | 5GB/month | $2.50 |
| S3 (Menu Images) | 10GB storage, 100GB transfer | $1 |
| Data Transfer | 100GB outbound | $9 |
| **Total** | | **$54.50-64.50** |

**Note**: 
- 무료 티어 적용 시 첫 12개월 일부 비용 절감 가능
- 실제 비용은 사용량에 따라 변동

---

### 5.2 Cost Optimization Tips

**1. Reserved Instances**:
- 1년 약정 시 EC2/RDS 비용 30-40% 절감

**2. Spot Instances** (개발 환경):
- 개발/테스트 환경에서 Spot Instance 사용 시 최대 90% 절감

**3. S3 Lifecycle Policy**:
- 오래된 이미지를 S3 Glacier로 이동하여 비용 절감

**4. CloudWatch Logs Retention**:
- 로그 보관 기간을 7일로 제한하여 비용 절감

---

## 6. Scalability Considerations

### 6.1 Vertical Scaling (단기)

**EC2 Instance Type Upgrade**:
```
t3.small (2 vCPU, 2GB) 
  → t3.medium (2 vCPU, 4GB) 
  → t3.large (2 vCPU, 8GB)
```

**RDS Instance Type Upgrade**:
```
db.t3.small (2 vCPU, 2GB) 
  → db.t3.medium (2 vCPU, 4GB) 
  → db.t3.large (2 vCPU, 8GB)
```

---

### 6.2 Horizontal Scaling (장기)

**향후 확장 시 고려사항**:

**1. Application Load Balancer 추가**:
- 다중 EC2 인스턴스 간 트래픽 분산
- Health Check 자동화
- SSL/TLS 종료

**2. Auto Scaling Group**:
- CPU 사용률 기반 자동 스케일링
- 최소 2개, 최대 5개 인스턴스

**3. RDS Read Replica**:
- 읽기 전용 복제본 추가
- 읽기 성능 향상

**4. ElastiCache (Redis)**:
- 메뉴 데이터 캐싱
- 세션 데이터 저장

---

## 7. Disaster Recovery

### 7.1 Backup Strategy

**RDS Automated Backups**:
- 일별 자동 백업 (03:00-04:00)
- 7일 보관
- Point-in-Time Recovery 지원

**Manual Snapshots** (권장):
- 주요 변경 전 수동 스냅샷 생성
- 무기한 보관 가능

---

### 7.2 Recovery Procedures

**RDS 복구**:
```bash
# 특정 시점으로 복구
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier tableorder-db \
  --target-db-instance-identifier tableorder-db-restored \
  --restore-time 2026-02-09T12:00:00Z
```

**EC2 복구**:
- AMI (Amazon Machine Image) 생성 권장
- 주기적으로 AMI 백업

---

## 8. Deployment Checklist

### 8.1 Initial Setup

- [ ] AWS 계정 생성 및 IAM 사용자 설정
- [ ] Default VPC 확인
- [ ] Security Groups 생성 (Backend, RDS)
- [ ] EC2 Key Pair 생성 (SSH 접근용)
- [ ] RDS PostgreSQL 인스턴스 생성
- [ ] EC2 인스턴스 생성 및 설정
- [ ] CloudWatch Logs Agent 설치 및 설정
- [ ] S3 Bucket 생성 (메뉴 이미지용)
- [ ] .env 파일 설정 (환경 변수)
- [ ] FastAPI 애플리케이션 배포
- [ ] Database 스키마 마이그레이션
- [ ] Health Check 엔드포인트 테스트
- [ ] CloudWatch Alarms 설정

---

### 8.2 Post-Deployment Verification

- [ ] API 엔드포인트 접근 테스트
- [ ] Database 연결 테스트
- [ ] 로그 수집 확인 (CloudWatch Logs)
- [ ] 메뉴 이미지 업로드 테스트 (S3)
- [ ] 성능 테스트 (API 응답 시간)
- [ ] 보안 그룹 규칙 검증
- [ ] 백업 설정 확인

---

## Infrastructure Summary

| 카테고리 | 서비스 | 스펙 | 목적 |
|----------|--------|------|------|
| Compute | AWS EC2 | t3.small (2 vCPU, 2GB) | Backend 서버 |
| Database | AWS RDS PostgreSQL | db.t3.small (2 vCPU, 2GB) | 데이터 저장 |
| Storage | AWS S3 | Standard | 메뉴 이미지 |
| Logging | AWS CloudWatch Logs | 7일 보관 | 로그 관리 |
| Monitoring | AWS CloudWatch | 기본 메트릭 | 성능 모니터링 |
| Networking | AWS VPC | Default VPC | 네트워크 격리 |
| Security | Security Groups | EC2, RDS | 접근 제어 |

**Total Services**: 7개 AWS 서비스

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
