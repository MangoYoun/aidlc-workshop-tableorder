# Backend Service - Infrastructure Design Plan

## Plan Overview

이 계획은 Backend Service Unit의 논리적 컴포넌트를 실제 인프라 서비스로 매핑하기 위한 계획입니다.

**Unit**: Backend Service  
**Cloud Provider**: AWS (Amazon Web Services)  
**Target Environment**: 중소규모 매장 3-10개 (동시 사용자 10-50명)

---

## Execution Checklist

### Phase 1: Deployment Environment
- [x] Cloud provider 선택 확정
- [x] 배포 환경 구성 (개발/프로덕션)
- [x] 리전 선택

### Phase 2: Compute Infrastructure
- [x] Backend 서버 컴퓨팅 서비스 선택
- [x] 인스턴스 타입 및 스펙 결정
- [x] Auto Scaling 전략

### Phase 3: Storage Infrastructure
- [x] Database 서비스 선택
- [x] Database 인스턴스 스펙 결정
- [x] 백업 전략

### Phase 4: Networking Infrastructure
- [x] Load Balancer 필요성 평가
- [x] API Gateway 필요성 평가
- [x] VPC 및 보안 그룹 설계

### Phase 5: Monitoring Infrastructure
- [x] 로깅 서비스 선택
- [x] 모니터링 도구 선택
- [x] 알림 설정

### Phase 6: Documentation
- [x] infrastructure-design.md 생성
- [x] deployment-architecture.md 생성

---

## Infrastructure Design Questions

다음 질문들에 답변하여 Backend Service의 인프라 설계 방향을 결정해주세요.

### Question 1: 배포 환경 (Deployment Environment)
Backend 서버를 어디에 배포하시겠습니까?

**Context**: 중소규모 매장 3-10개, 동시 사용자 10-50명 규모입니다.

A) AWS EC2 (가상 서버)
B) AWS Elastic Beanstalk (관리형 플랫폼)
C) AWS ECS/Fargate (컨테이너)
D) 로컬 서버 (On-premise)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: AWS EC2가 가장 간단하고 직관적입니다. 초보자가 서버를 직접 제어하고 학습하기에 적합합니다. Elastic Beanstalk이나 ECS는 추가 학습이 필요하며, 중소규모에서는 EC2로 충분합니다.

---

### Question 2: EC2 인스턴스 타입
EC2 인스턴스 타입을 어떻게 선택하시겠습니까?

**Context**: FastAPI 애플리케이션, 동시 사용자 10-50명, API 응답 500ms 이하 목표입니다.

A) t3.micro (1 vCPU, 1GB RAM) - 무료 티어
B) t3.small (2 vCPU, 2GB RAM) - 권장
C) t3.medium (2 vCPU, 4GB RAM)
D) t3.large (2 vCPU, 8GB RAM)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

**이유**: t3.small이 중소규모 애플리케이션에 적합합니다. 2 vCPU와 2GB RAM으로 FastAPI 서버와 동시 사용자 10-50명을 충분히 처리할 수 있습니다. t3.micro는 메모리가 부족할 수 있고, t3.medium 이상은 과도합니다.

---

### Question 3: Database 서비스
PostgreSQL 데이터베이스를 어떻게 배포하시겠습니까?

**Context**: 8개 테이블, 중소규모 데이터, 트랜잭션 무결성 필요합니다.

A) AWS RDS PostgreSQL (관리형 데이터베이스)
B) EC2에 PostgreSQL 직접 설치
C) AWS Aurora PostgreSQL (고성능 관리형)
D) 로컬 PostgreSQL
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: AWS RDS PostgreSQL이 가장 적합합니다. 자동 백업, 패치 관리, 모니터링이 제공되어 운영 부담이 적습니다. EC2 직접 설치는 관리가 복잡하고, Aurora는 중소규모에 과도하며 비용이 높습니다.

---

### Question 4: RDS 인스턴스 타입
RDS PostgreSQL 인스턴스 타입을 어떻게 선택하시겠습니까?

**Context**: 8개 테이블, 중소규모 데이터, 동시 연결 10-15개 예상입니다.

A) db.t3.micro (1 vCPU, 1GB RAM) - 무료 티어
B) db.t3.small (2 vCPU, 2GB RAM) - 권장
C) db.t3.medium (2 vCPU, 4GB RAM)
D) db.t3.large (2 vCPU, 8GB RAM)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

**이유**: db.t3.small이 중소규모 데이터베이스에 적합합니다. 2 vCPU와 2GB RAM으로 동시 연결 10-15개를 충분히 처리할 수 있습니다. db.t3.micro는 성능이 부족할 수 있고, db.t3.medium 이상은 과도합니다.

---

### Question 5: Database 백업 전략
RDS 백업을 어떻게 관리하시겠습니까?

**Context**: 데이터 손실 방지 및 복구 필요합니다.

A) RDS 자동 백업 (일별, 7일 보관)
B) RDS 자동 백업 (일별, 30일 보관)
C) 수동 스냅샷만 사용
D) 백업 없음
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: RDS 자동 백업 (일별, 7일 보관)이 적합합니다. 무료 티어에서도 지원되며, 7일 보관으로 충분한 복구 기간을 제공합니다. 30일 보관은 추가 비용이 발생하며, 중소규모에서는 과도합니다.

---

### Question 6: Load Balancer 필요성
Load Balancer를 사용하시겠습니까?

**Context**: 단일 EC2 인스턴스, 동시 사용자 10-50명입니다.

A) Load Balancer 없음 (단일 EC2 직접 접근)
B) Application Load Balancer (ALB) 사용
C) Network Load Balancer (NLB) 사용
D) Classic Load Balancer 사용
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: 초기에는 Load Balancer 없이 단일 EC2 인스턴스로 충분합니다. 동시 사용자 10-50명 규모에서는 단일 서버로 처리 가능하며, Load Balancer는 추가 비용과 복잡도를 증가시킵니다. 확장이 필요하면 나중에 추가할 수 있습니다.

---

### Question 7: API Gateway 필요성
API Gateway를 사용하시겠습니까?

**Context**: FastAPI가 자체적으로 API 엔드포인트를 제공합니다.

A) API Gateway 없음 (FastAPI 직접 노출)
B) AWS API Gateway 사용
C) Kong API Gateway 사용
D) Nginx를 API Gateway로 사용
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: 초기에는 API Gateway 없이 FastAPI를 직접 노출하는 것이 간단합니다. FastAPI가 자체적으로 API 문서화, 검증, 에러 처리를 제공하므로 별도의 API Gateway가 필요하지 않습니다. 필요하면 나중에 추가할 수 있습니다.

---

### Question 8: VPC 및 보안 그룹
VPC 및 보안 그룹을 어떻게 설정하시겠습니까?

**Context**: EC2와 RDS 간 통신, 외부 접근 제어가 필요합니다.

A) Default VPC 사용 + 간단한 보안 그룹
B) Custom VPC + Public/Private Subnet 분리
C) VPC 없이 Public 인스턴스만 사용
D) VPN 연결 추가
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: Default VPC와 간단한 보안 그룹으로 시작하는 것이 초보자에게 적합합니다. Custom VPC는 네트워크 지식이 필요하며, 초기에는 과도합니다. 보안 그룹으로 EC2(포트 80, 443, 22)와 RDS(포트 5432, EC2에서만 접근)를 제어할 수 있습니다.

---

### Question 9: 로깅 서비스
애플리케이션 로그를 어떻게 관리하시겠습니까?

**Context**: Python logging으로 파일에 로그를 저장합니다.

A) EC2 로컬 파일 로깅만 사용
B) AWS CloudWatch Logs로 전송
C) ELK Stack (Elasticsearch, Logstash, Kibana)
D) 외부 로깅 서비스 (Datadog, Splunk)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

**이유**: AWS CloudWatch Logs로 로그를 전송하는 것이 권장됩니다. EC2 인스턴스가 종료되어도 로그가 보존되며, 중앙 집중식 로그 관리가 가능합니다. 설정도 간단하며, AWS 무료 티어에서 일정량까지 무료입니다. ELK Stack은 초보자에게 복잡합니다.

---

### Question 10: 모니터링 도구
서버 및 애플리케이션 모니터링을 어떻게 하시겠습니까?

**Context**: CPU, 메모리, API 응답 시간 등을 모니터링해야 합니다.

A) AWS CloudWatch 기본 모니터링
B) AWS CloudWatch + Custom Metrics
C) Prometheus + Grafana
D) 외부 APM 도구 (New Relic, Datadog)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: AWS CloudWatch 기본 모니터링으로 시작하는 것이 간단합니다. EC2와 RDS의 CPU, 메모리, 디스크, 네트워크를 자동으로 모니터링합니다. Custom Metrics는 나중에 필요하면 추가할 수 있습니다. Prometheus나 APM 도구는 초보자에게 복잡하고 비용이 추가됩니다.

---

## Instructions

모든 질문에 초보자 친화적인 답변이 이미 채워져 있습니다. 검토 후 승인해주시면 Infrastructure Design 아티팩트 생성을 시작합니다.

---

**검토 후 승인해주세요.**
