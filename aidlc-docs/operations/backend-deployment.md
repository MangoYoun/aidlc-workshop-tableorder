# Backend Service Deployment Guide

## Overview

Backend Service (FastAPI + PostgreSQL)를 AWS EC2 + RDS에 배포하는 상세 가이드입니다.

**소요 시간**: 1-1.5시간  
**예상 비용**: $54-65/월

---

## Step 1: RDS PostgreSQL 생성

### 1.1 AWS Console에서 RDS 생성

1. AWS Console → RDS → Create database
2. 설정:
   - Engine: PostgreSQL 14.x
   - Template: Free tier (또는 Dev/Test)
   - DB instance identifier: `tableorder-db`
   - Master username: `admin`
   - Master password: `{strong-password}` (기록 필수!)
   - DB instance class: db.t3.small
   - Storage: 20GB gp3
   - Multi-AZ: No
   - VPC: Default VPC
   - Public access: No
   - VPC security group: Create new → `tableorder-rds-sg`
   - Backup retention: 7 days

3. Create database 클릭
4. 생성 완료 대기 (약 5-10분)

### 1.2 RDS Endpoint 확인

```bash
# RDS Endpoint 확인
aws rds describe-db-instances \
  --db-instance-identifier tableorder-db \
  --query "DBInstances[0].Endpoint.Address" \
  --output text

# 출력 예시: tableorder-db.c1234567890.ap-northeast-2.rds.amazonaws.com
```

**Endpoint를 기록하세요!** (나중에 .env 파일에 사용)

---

## Step 2: EC2 Security Group 생성

### 2.1 Backend EC2 Security Group

```bash
# Security Group 생성
aws ec2 create-security-group \
  --group-name tableorder-backend-sg \
  --description "Security group for TableOrder Backend" \
  --vpc-id {your-vpc-id}

# HTTP 허용 (80)
aws ec2 authorize-security-group-ingress \
  --group-id {sg-id} \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

# HTTPS 허용 (443)
aws ec2 authorize-security-group-ingress \
  --group-id {sg-id} \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

# SSH 허용 (22) - 본인 IP만
aws ec2 authorize-security-group-ingress \
  --group-id {sg-id} \
  --protocol tcp \
  --port 22 \
  --cidr {your-ip}/32
```

### 2.2 RDS Security Group 업데이트

```bash
# RDS Security Group에 EC2 접근 허용
aws ec2 authorize-security-group-ingress \
  --group-id {rds-sg-id} \
  --protocol tcp \
  --port 5432 \
  --source-group {backend-sg-id}
```

---

## Step 3: EC2 인스턴스 생성

### 3.1 Key Pair 생성 (최초 1회)

```bash
# Key Pair 생성
aws ec2 create-key-pair \
  --key-name tableorder-key \
  --query 'KeyMaterial' \
  --output text > tableorder-key.pem

# 권한 설정
chmod 400 tableorder-key.pem
```

### 3.2 EC2 인스턴스 생성

```bash
# Ubuntu 22.04 AMI ID 확인
aws ec2 describe-images \
  --owners 099720109477 \
  --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" \
  --query 'Images[0].ImageId' \
  --output text

# EC2 인스턴스 생성
aws ec2 run-instances \
  --image-id {ami-id} \
  --instance-type t3.small \
  --key-name tableorder-key \
  --security-group-ids {backend-sg-id} \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=tableorder-backend}]'
```

### 3.3 Public IP 확인

```bash
# Public IP 확인
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=tableorder-backend" \
  --query "Reservations[0].Instances[0].PublicIpAddress" \
  --output text

# 출력 예시: 52.79.123.456
```

**Public IP를 기록하세요!**

---

## Step 4: EC2 인스턴스 설정

### 4.1 SSH 접속

```bash
ssh -i tableorder-key.pem ubuntu@{ec2-public-ip}
```

### 4.2 시스템 업데이트 및 패키지 설치

```bash
# 시스템 업데이트
sudo apt-get update
sudo apt-get upgrade -y

# Python 및 필수 패키지 설치
sudo apt-get install -y python3.9 python3-pip python3-venv git nginx

# PostgreSQL 클라이언트 설치 (테스트용)
sudo apt-get install -y postgresql-client
```

### 4.3 애플리케이션 디렉토리 생성

```bash
# 애플리케이션 디렉토리 생성
sudo mkdir -p /opt/tableorder
sudo chown ubuntu:ubuntu /opt/tableorder
cd /opt/tableorder

# 로그 디렉토리 생성
sudo mkdir -p /var/log/tableorder
sudo chown ubuntu:ubuntu /var/log/tableorder
```

---

## Step 5: 애플리케이션 배포

### 5.1 코드 업로드

**방법 1: Git Clone (권장)**
```bash
cd /opt/tableorder
git clone {your-repo-url} .
```

**방법 2: SCP로 파일 전송**
```bash
# 로컬에서 실행
scp -i tableorder-key.pem -r src/ ubuntu@{ec2-public-ip}:/opt/tableorder/
scp -i tableorder-key.pem config/requirements.txt ubuntu@{ec2-public-ip}:/opt/tableorder/
```

### 5.2 Python 가상 환경 생성

```bash
cd /opt/tableorder
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install --upgrade pip
pip install -r config/requirements.txt
```

### 5.3 환경 변수 설정

```bash
# .env 파일 생성
cat > /opt/tableorder/.env <<EOF
# Database
DATABASE_URL=postgresql://admin:{password}@{rds-endpoint}:5432/tableorder

# JWT
JWT_SECRET_KEY=$(openssl rand -hex 32)
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
EOF

# 권한 설정
chmod 600 /opt/tableorder/.env
```

**중요**: `{password}`, `{rds-endpoint}`, `{account-id}` 를 실제 값으로 교체하세요!

---

## Step 6: Database 초기화

### 6.1 Database 연결 테스트

```bash
# PostgreSQL 연결 테스트
psql -h {rds-endpoint} -U admin -d postgres

# 비밀번호 입력 후 연결 확인
# \q 로 종료
```

### 6.2 Database 생성

```bash
# tableorder 데이터베이스 생성
psql -h {rds-endpoint} -U admin -d postgres -c "CREATE DATABASE tableorder;"
```

### 6.3 스키마 마이그레이션

```bash
cd /opt/tableorder
source venv/bin/activate

# FastAPI 앱 실행하여 자동 스키마 생성
python -c "from src.database import engine, Base; from src.models import *; Base.metadata.create_all(bind=engine)"

# 또는 Alembic 사용 (설정된 경우)
# alembic upgrade head
```

---

## Step 7: Systemd 서비스 설정

### 7.1 Systemd 서비스 파일 생성

```bash
sudo cat > /etc/systemd/system/tableorder.service <<EOF
[Unit]
Description=TableOrder FastAPI Application
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/tableorder
Environment="PATH=/opt/tableorder/venv/bin"
ExecStart=/opt/tableorder/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

### 7.2 서비스 시작

```bash
# Systemd 리로드
sudo systemctl daemon-reload

# 서비스 활성화 (부팅 시 자동 시작)
sudo systemctl enable tableorder

# 서비스 시작
sudo systemctl start tableorder

# 상태 확인
sudo systemctl status tableorder

# 로그 확인
sudo journalctl -u tableorder -f
```

---

## Step 8: Nginx 리버스 프록시 설정

### 8.1 Nginx 설정 파일 생성

```bash
sudo cat > /etc/nginx/sites-available/tableorder <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # SSE 지원
        proxy_buffering off;
        proxy_cache off;
        proxy_set_header Connection '';
        proxy_http_version 1.1;
        chunked_transfer_encoding off;
    }
}
EOF
```

### 8.2 Nginx 활성화

```bash
# 기본 사이트 비활성화
sudo rm /etc/nginx/sites-enabled/default

# TableOrder 사이트 활성화
sudo ln -s /etc/nginx/sites-available/tableorder /etc/nginx/sites-enabled/

# 설정 테스트
sudo nginx -t

# Nginx 재시작
sudo systemctl restart nginx
```

---

## Step 9: 배포 확인

### 9.1 Health Check

```bash
# 로컬에서 확인
curl http://localhost:8000/health

# 외부에서 확인
curl http://{ec2-public-ip}/health

# 예상 응답: {"status":"healthy"}
```

### 9.2 API 엔드포인트 테스트

```bash
# 메뉴 조회 (store_id=1 가정)
curl http://{ec2-public-ip}/api/menus?store_id=1

# 예상 응답: [] (빈 배열, 아직 메뉴 없음)
```

---

## Step 10: CloudWatch Logs 설정 (선택사항)

### 10.1 CloudWatch Logs Agent 설치

```bash
# Agent 다운로드
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb

# 설치
sudo dpkg -i amazon-cloudwatch-agent.deb
```

### 10.2 Agent 설정

```bash
sudo cat > /opt/aws/amazon-cloudwatch-agent/etc/config.json <<EOF
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

# Agent 시작
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -s \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/config.json
```

---

## Troubleshooting

### Issue 1: Database 연결 실패

**증상**: `psycopg2.OperationalError: could not connect to server`

**해결**:
1. RDS Security Group 확인 (EC2 SG에서 5432 포트 허용)
2. DATABASE_URL 확인 (.env 파일)
3. RDS 엔드포인트 확인

### Issue 2: Systemd 서비스 시작 실패

**증상**: `systemctl status tableorder` 에서 failed 상태

**해결**:
```bash
# 로그 확인
sudo journalctl -u tableorder -n 50

# 수동 실행으로 에러 확인
cd /opt/tableorder
source venv/bin/activate
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Issue 3: Nginx 502 Bad Gateway

**증상**: `curl http://{ec2-public-ip}` 에서 502 에러

**해결**:
1. FastAPI 서비스 상태 확인: `sudo systemctl status tableorder`
2. 포트 8000 리스닝 확인: `sudo netstat -tlnp | grep 8000`
3. Nginx 에러 로그 확인: `sudo tail -f /var/log/nginx/error.log`

---

## Post-Deployment Checklist

- [ ] RDS PostgreSQL 생성 완료
- [ ] EC2 인스턴스 생성 완료
- [ ] Security Groups 설정 완료
- [ ] FastAPI 애플리케이션 배포 완료
- [ ] Database 스키마 생성 완료
- [ ] Systemd 서비스 실행 중
- [ ] Nginx 리버스 프록시 설정 완료
- [ ] Health Check 엔드포인트 정상 응답
- [ ] API 엔드포인트 정상 응답
- [ ] CloudWatch Logs 설정 완료 (선택사항)

---

## Next Steps

1. **Frontend 배포**: `frontend-deployment.md` 참조
2. **통합 테스트**: Frontend와 Backend 연동 테스트
3. **모니터링 설정**: CloudWatch Alarms 설정
4. **보안 강화**: SSL/TLS 인증서 설정 (Let's Encrypt)

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
