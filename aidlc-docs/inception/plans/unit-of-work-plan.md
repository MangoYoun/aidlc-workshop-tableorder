# Unit of Work Plan

## Plan Overview

이 계획은 테이블오더 서비스를 관리 가능한 작업 단위(Units of Work)로 분해하기 위한 계획입니다.

---

## Execution Checklist

### Phase 1: Unit Identification
- [x] 시스템 분해 전략 결정
- [x] Unit 경계 식별
- [x] 각 Unit의 책임 정의
- [x] Unit 간 의존성 분석

### Phase 2: Story Mapping
- [x] User Stories를 Unit에 매핑
- [x] Epic별 Unit 할당 확인
- [x] Story 의존성 검증

### Phase 3: Dependency Analysis
- [x] Unit 간 의존성 매트릭스 생성
- [x] 통신 패턴 정의
- [x] 데이터 공유 방식 정의

### Phase 4: Code Organization (Greenfield)
- [x] 배포 모델 결정
- [x] 디렉토리 구조 정의
- [x] 코드 조직 전략 문서화

### Phase 5: Documentation
- [x] unit-of-work.md 파일 생성
- [x] unit-of-work-dependency.md 파일 생성
- [x] unit-of-work-story-map.md 파일 생성
- [x] Unit 경계 및 의존성 검증

---

## Unit of Work Questions

다음 질문들에 답변하여 시스템 분해 방향을 결정해주세요.

### Question 1: System Decomposition Strategy
시스템을 어떻게 분해하시겠습니까?

A) Monolithic (단일 Unit) - Frontend + Backend를 하나의 Unit으로
B) Frontend/Backend Split (2 Units) - Frontend Unit + Backend Unit
C) Multi-Service (3+ Units) - Customer Frontend + Admin Frontend + Backend
D) Microservices (4+ Units) - 기능별로 세분화된 독립 서비스
E) Other (please describe after [Answer]: tag below)

[Answer]: C

**이유**: Customer App과 Admin App은 사용자가 다르고 기능이 명확히 구분되므로 별도 Unit으로 관리하는 것이 좋습니다. Backend는 공통 API를 제공하는 하나의 Unit으로 유지합니다. 

---

### Question 2: Deployment Model (if multiple units)
여러 Unit으로 분해하는 경우, 배포 모델은 어떻게 하시겠습니까?

A) Monorepo - 하나의 저장소에 모든 Unit
B) Multi-repo - Unit별로 별도 저장소
C) Not applicable (단일 Unit인 경우)
D) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: 초보자에게는 Monorepo가 관리하기 쉽습니다. 모든 코드가 한 곳에 있어 변경사항 추적이 용이하고, 공통 설정을 공유할 수 있습니다. 

---

### Question 3: Frontend Unit Organization
Frontend를 어떻게 조직하시겠습니까?

A) Single Frontend App - Customer + Admin을 하나의 앱으로 (라우팅으로 분리)
B) Separate Frontend Apps - Customer App과 Admin App을 별도 Unit으로
C) Shared Components - 공통 컴포넌트 라이브러리 + 2개 앱
D) Other (please describe after [Answer]: tag below)

[Answer]: B

**이유**: Customer와 Admin은 사용자 경험이 완전히 다르므로 별도 앱으로 분리하는 것이 명확합니다. 각 앱을 독립적으로 개발하고 배포할 수 있습니다. 

---

### Question 4: Backend Unit Organization
Backend를 어떻게 조직하시겠습니까?

A) Single Backend Service - 모든 API를 하나의 서비스로
B) API Gateway + Services - API Gateway + 기능별 서비스
C) Modular Monolith - 하나의 서비스 내에서 모듈로 분리
D) Other (please describe after [Answer]: tag below)

[Answer]: C

**이유**: Modular Monolith는 초보자에게 적합합니다. 하나의 서비스로 배포가 간단하면서도, 내부적으로 모듈(auth, menu, order, table)로 논리적 분리가 가능합니다. 

---

### Question 5: Database Unit Organization
Database를 어떻게 조직하시겠습니까?

A) Single Database - 모든 테이블을 하나의 데이터베이스에
B) Database per Service - Unit별로 별도 데이터베이스
C) Shared Database with Schemas - 하나의 DB, Unit별 스키마
D) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: 단일 데이터베이스가 가장 간단합니다. 트랜잭션 관리가 쉽고, 조인 쿼리가 가능하며, 초보자가 관리하기 용이합니다. 

---

### Question 6: Story Grouping Strategy
User Stories를 Unit에 어떻게 그룹화하시겠습니까?

A) By Epic - Epic별로 Unit 할당
B) By Persona - Persona별로 Unit 할당 (Customer Unit, Admin Unit)
C) By Layer - Layer별로 Unit 할당 (Frontend Unit, Backend Unit)
D) By Feature - 기능별로 Unit 할당
E) Other (please describe after [Answer]: tag below)

[Answer]: B

**이유**: Persona별 그룹화가 가장 명확합니다. Epic 1 (고객 주문 여정) → Customer Frontend Unit, Epic 2 (관리자 운영 여정) → Admin Frontend Unit, Epic 3 (NFR) → Backend Unit 

---

### Question 7: Unit Development Order
Unit 개발 순서를 어떻게 하시겠습니까?

A) Sequential - Unit을 순차적으로 개발 (Backend → Frontend)
B) Parallel - Unit을 병렬로 개발
C) Iterative - 모든 Unit을 동시에 반복적으로 개발
D) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: 초보자에게는 순차적 개발이 적합합니다. Backend API를 먼저 완성한 후 Frontend를 개발하면 API 명세가 명확하고 통합이 쉽습니다. 

---

### Question 8: Shared Code Strategy
공통 코드(모델, 유틸리티 등)를 어떻게 관리하시겠습니까?

A) Duplicate - 각 Unit에 복사
B) Shared Library - 별도의 공유 라이브러리 Unit
C) Copy on Write - 필요시 복사하여 사용
D) Not applicable (단일 Unit인 경우)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: 초보자에게는 각 Unit에 필요한 코드를 복사하는 것이 가장 간단합니다. 의존성 관리가 필요 없고, 각 Unit이 독립적으로 동작합니다. (Frontend의 DTO 모델 등) 

---

### Question 9: Integration Testing Strategy
Unit 간 통합 테스트를 어떻게 하시겠습니까?

A) End-to-End Tests - 전체 시스템 통합 테스트
B) Contract Tests - Unit 간 계약 테스트
C) Integration Tests per Unit - Unit별 통합 테스트
D) Not applicable (단일 Unit인 경우)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: End-to-End 테스트가 가장 직관적입니다. 실제 사용자 시나리오를 테스트하여 전체 시스템이 제대로 동작하는지 확인할 수 있습니다. 

---

### Question 10: Unit Complexity
각 Unit의 복잡도를 어떻게 평가하시겠습니까?

A) By Story Count - Story 개수로 평가
B) By Component Count - 컴포넌트 개수로 평가
C) By Development Time - 예상 개발 시간으로 평가
D) Equal Complexity - 모든 Unit 동일한 복잡도로 간주
E) Other (please describe after [Answer]: tag below)

[Answer]: A

**이유**: Story 개수로 평가하는 것이 가장 객관적입니다. Epic 1 (5 stories) → Customer Frontend, Epic 2 (4 stories) → Admin Frontend, Epic 3 (3 stories) → Backend로 복잡도를 쉽게 파악할 수 있습니다. 

---

## Instructions

1. 위의 모든 질문에 [Answer]: 태그 뒤에 선택한 옵션의 문자(A, B, C 등)를 입력해주세요.
2. 제공된 옵션이 맞지 않으면 마지막 옵션을 선택하고 설명을 추가해주세요.
3. 모든 질문에 답변하신 후 "완료" 또는 "done"이라고 말씀해주세요.
4. 답변 완료 후, 이 계획을 검토하고 승인해주시면 Units Generation을 시작합니다.

---

**모든 질문에 답변하신 후 "완료" 또는 "done"이라고 말씀해주세요.**
