# Deployment Architecture - Backend Service

## Overview

Backend Service의 배포 아키텍처와 배포 프로세스를 정의합니다.

**Deployment Model**: Single-Region, Single-AZ (초기 구성)  
**Cloud Provider**: AWS  
**Region**: ap-northeast-2 (Seoul)

---

## 1. Deployment Environments

### 1.1 Development Environment

**목적**: 로컬 개발 및 테스트

**Infrastructure**:
- **Backend**: 로컬 머신 (localhost:8000)
- **Database**: 로컬 PostgreSQL 또는 Docker
- **Storage**: 로컬 파일 시스템

**Configuration**:
```bash
# .env.development
DATABASE_URL=postgresql://user:password@localhost:5432/tableorder_dev
ENVIRONMENT=development
FRONTEND_URL=http://localhost:3000
LOG_LEVEL=DEBUG
```

---

### 1.2 Production Environment

**목적**: 실제 서비스 운영

**Infrastructure**:
- **Backend**: AWS EC2 (t3.small)
- **Database**: AWS RDS PostgreSQL (db.t3.small)
- **Storage**: AWS S3

**Configuration**:
```bash
# .env.production
DATABASE_URL=postgresql://user:password@{rds-endpoint}:5432/tableorder
ENVIRONMENT=production
FRONTEND_URL=https://your-frontend-domain.com
LOG_LEVEL=INFO
```

---

## 2. Deployment Process

### 2.1 Initial Deployment (첫 배포)

**Step 1: AWS 리소스 생성**

```bash
# 1. RDS PostgreSQL 생성
aws rds create-db-instance \
  --db-instance-identifier tableorder-db \
  --db-instance-class db.t3.small \
  --engine postgres \
  --engine-version 14.x \
  --master-username admin \
  --master-user-password {strong-password} \
  --allocated-storage 20 \
  --backup-retention-period 7 \
  --no-multi-az \
  --publicly-accessible false \
  --vpc-security-group-ids {rds-sg-id}

# 2. EC2 인스턴스 생성
aws ec2 run-instances \
  --image-id ami-0c9c942bd7bf113a2 \
  --instance-type t3.small \
  --key-name {your-key-pair} \
  --security-group-ids {backend-sg-id} \
  --iam-instance-profile Name=tableorder-ec2-role \
  --user-data file://user-data.sh \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=tableorder-backend}]'

# 3. S3 Bucket 생성
aws s3 mb s3://tableorder-menu-images-{account-id} --region ap-northeast-2
```

**Step 2: EC2 인스턴스 설정**

```bash
# SSH 접속
ssh -i {your-key.pem} ubuntu@{ec2-public-ip}

# 애플리케이션 디렉토리 생성
mkdir -p /opt/tableorder
cd /opt/tableorder

# Git 저장소 클론 (또는 파일 업로드)
git clone {your-repo-url} .

# Python 가상 환경 생성
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# .env 파일 생성
cat > .env <<EOF
DATABASE_URL=postgresql://admin:{password}@{rds-endpoint}:5432/tableorder
JWT_SECRET_KEY={strong-random-key}
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=16
SESSION_EXPIRE_HOURS=16
SESSION_LAST_ORDER_TIMEOUT_HOURS=2
ENVIRONMENT=production
FRONTEND_URL=https://your-frontend-domain.com
LOG_LEVEL=INFO
LOG_FILE=/var/log/tableorder/app.log
AWS_REGION=ap-northeast-2
S3_BUCKET_NAME=tableorder-menu-images-{account-id}
EOF

# 로그 디렉토리 생성
mkdir -p /var/log/tableorder
```

**Step 3: Database 마이그레이션**

```bash
# Alembic 마이그레이션 실행 (또는 직접 스키마 생성)
alembic upgrade head

# 또는 직접 스키마 생성
python scripts/create_schema.py
```

**Step 4: 애플리케이션 시작**

```bash
# Systemd 서비스 파일 생성
cat > /etc/systemd/system/tableorder.service <<EOF
[Unit]
Description=TableOrder FastAPI Application
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/tableorder
Environment="PATH=/opt/tableorder/venv/bin"
ExecStart=/opt/tableorder/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 서비스 시작
systemctl daemon-reload
systemctl enable tableorder
systemctl start tableorder

# 상태 확인
systemctl status tableorder
```

**Step 5: Nginx 설정 (리버스 프록시)**

```bash
# Nginx 설치
apt-get install -y nginx

# Nginx 설정
cat > /etc/nginx/sites-available/tableorder <<EOF
server {
    listen 80;
    server_name {your-domain-or-ip};

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# 설정 활성화
ln -s /etc/nginx/sites-available/tableorder /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

---

### 2.2 Continuous Deployment (지속적 배포)

**배포 프로세스**:

```bash
# 1. SSH 접속
ssh -i {your-key.pem} ubuntu@{ec2-public-ip}

# 2. 애플리케이션 디렉토리로 이동
cd /opt/tableorder

# 3. 최신 코드 가져오기
git pull origin main

# 4. 의존성 업데이트 (필요시)
source venv/bin/activate
pip install -r requirements.txt

# 5. Database 마이그레이션 (필요시)
alembic upgrade head

# 6. 애플리케이션 재시작
systemctl restart tableorder

# 7. 상태 확인
systemctl status tableorder
curl http://localhost:8000/health
```

---

## 3. Rollback Strategy

### 3.1 Application Rollback

```bash
# 1. 이전 버전으로 Git 롤백
cd /opt/tableorder
git log --oneline  # 이전 커밋 확인
git checkout {previous-commit-hash}

# 2. 애플리케이션 재시작
systemctl restart tableorder

# 3. 상태 확인
systemctl status tableorder
```

---

### 3.2 Database Rollback

```bash
# RDS Point-in-Time Recovery
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier tableorder-db \
  --target-db-instance-identifier tableorder-db-restored \
  --restore-time {timestamp-before-issue}

# 복구된 인스턴스로 전환
# 1. 애플리케이션 중지
# 2. .env 파일의 DATABASE_URL 업데이트
# 3. 애플리케이션 재시작
```

---

## 4. Monitoring and Alerting

### 4.1 CloudWatch Alarms

```bash
# EC2 CPU 알람 생성
aws cloudwatch put-metric-alarm \
  --alarm-name tableorder-backend-high-cpu \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=InstanceId,Value={instance-id}

# RDS Connection 알람 생성
aws cloudwatch put-metric-alarm \
  --alarm-name tableorder-rds-high-connections \
  --alarm-description "Alert when connections exceed 10" \
  --metric-name DatabaseConnections \
  --namespace AWS/RDS \
  --statistic Average \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=DBInstanceIdentifier,Value=tableorder-db
```

---

### 4.2 Log Monitoring

```bash
# CloudWatch Logs Insights 쿼리 예시

# 1. 에러 로그 조회
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 100

# 2. 느린 API 조회 (500ms 초과)
fields @timestamp, @message
| filter @message like /Slow API/
| sort @timestamp desc
| limit 50

# 3. 특정 시간대 로그 조회
fields @timestamp, @message
| filter @timestamp >= "2026-02-09T12:00:00" and @timestamp <= "2026-02-09T13:00:00"
| sort @timestamp desc
```

---

## 5. Security Hardening

### 5.1 EC2 Security

```bash
# 1. 불필요한 포트 닫기
# Security Group에서 필요한 포트만 열기 (80, 443, 22)

# 2. SSH Key 기반 인증만 허용
# /etc/ssh/sshd_config
PasswordAuthentication no
PubkeyAuthentication yes

# 3. Fail2ban 설치 (SSH 브루트포스 방지)
apt-get install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban

# 4. 자동 보안 업데이트 활성화
apt-get install -y unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades
```

---

### 5.2 RDS Security

```bash
# 1. Public Access 비활성화 (이미 설정됨)
# 2. Security Group으로 EC2에서만 접근 허용 (이미 설정됨)
# 3. SSL/TLS 연결 강제 (선택사항)

# RDS SSL 인증서 다운로드
wget https://truststore.pki.rds.amazonaws.com/ap-northeast-2/ap-northeast-2-bundle.pem

# DATABASE_URL에 SSL 파라미터 추가
DATABASE_URL=postgresql://user:password@{rds-endpoint}:5432/tableorder?sslmode=require&sslrootcert=/path/to/ap-northeast-2-bundle.pem
```

---

## 6. Disaster Recovery Plan

### 6.1 Backup Verification

```bash
# RDS 백업 목록 확인
aws rds describe-db-snapshots \
  --db-instance-identifier tableorder-db

# 수동 스냅샷 생성
aws rds create-db-snapshot \
  --db-instance-identifier tableorder-db \
  --db-snapshot-identifier tableorder-db-manual-snapshot-$(date +%Y%m%d)
```

---

### 6.2 Recovery Testing

**분기별 복구 테스트 권장**:

```bash
# 1. 테스트용 RDS 인스턴스 복구
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier tableorder-db-test \
  --db-snapshot-identifier {snapshot-id}

# 2. 테스트 EC2 인스턴스에서 연결 테스트
# 3. 데이터 무결성 검증
# 4. 테스트 완료 후 리소스 삭제
```

---

## 7. Performance Optimization

### 7.1 Application Optimization

```bash
# 1. Uvicorn Workers 증가 (CPU 코어 수에 맞춤)
ExecStart=/opt/tableorder/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2

# 2. Gunicorn 사용 (프로덕션 권장)
pip install gunicorn
ExecStart=/opt/tableorder/venv/bin/gunicorn main:app -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

### 7.2 Database Optimization

```bash
# PostgreSQL 설정 튜닝 (RDS Parameter Group)
# 1. shared_buffers: 512MB (메모리의 25%)
# 2. effective_cache_size: 1.5GB (메모리의 75%)
# 3. work_mem: 16MB
# 4. maintenance_work_mem: 128MB
```

---

## 8. Deployment Checklist

### Pre-Deployment

- [ ] 코드 리뷰 완료
- [ ] 단위 테스트 통과
- [ ] 통합 테스트 통과
- [ ] Database 마이그레이션 스크립트 준비
- [ ] 환경 변수 확인
- [ ] 백업 생성 (RDS 스냅샷)

### Deployment

- [ ] 애플리케이션 중지 (또는 Blue-Green 배포)
- [ ] 최신 코드 배포
- [ ] Database 마이그레이션 실행
- [ ] 애플리케이션 시작
- [ ] Health Check 확인

### Post-Deployment

- [ ] API 엔드포인트 테스트
- [ ] 로그 확인 (에러 없는지)
- [ ] 성능 모니터링 (응답 시간)
- [ ] 사용자 피드백 수집
- [ ] 롤백 계획 준비

---

## Deployment Architecture Summary

| 단계 | 작업 | 도구/서비스 |
|------|------|-------------|
| 1. 인프라 생성 | AWS 리소스 프로비저닝 | AWS CLI, Console |
| 2. 애플리케이션 배포 | 코드 배포 및 설정 | Git, SSH |
| 3. Database 마이그레이션 | 스키마 업데이트 | Alembic, SQL |
| 4. 서비스 시작 | 애플리케이션 실행 | Systemd, Uvicorn |
| 5. 모니터링 설정 | 알람 및 로그 설정 | CloudWatch |
| 6. 보안 강화 | 보안 설정 적용 | Security Groups, IAM |

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
