# Requirements Verification Questions

요구사항을 명확히 하기 위한 질문입니다. 각 질문에 대해 [Answer]: 태그 뒤에 선택한 옵션의 문자를 입력해주세요.

---

## Question 1
Backend 개발에 사용할 프레임워크는 무엇인가요?

A) Spring Boot (Java)
B) Express.js (Node.js)
C) FastAPI (Python)
D) Django (Python)
E) ASP.NET Core (C#)
F) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Question 2
Frontend 개발에 사용할 프레임워크는 무엇인가요?

A) React
B) Vue.js
C) Angular
D) Svelte
E) Vanilla JavaScript (프레임워크 없음)
F) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 3
데이터베이스는 어떤 것을 사용하시겠습니까?

A) PostgreSQL
B) MySQL
C) MongoDB
D) DynamoDB (AWS)
E) SQLite
F) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 4
배포 환경은 어디인가요?

A) AWS (Amazon Web Services)
B) Azure (Microsoft)
C) GCP (Google Cloud Platform)
D) On-premises (자체 서버)
E) Local development only (로컬 개발만)
F) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 5
예상되는 동시 사용자 수는 얼마나 되나요?

A) 10명 이하 (소규모 매장 1-2개)
B) 10-50명 (중소규모 매장 3-10개)
C) 50-200명 (중대규모 매장 10-30개)
D) 200명 이상 (대규모 체인점)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 6
API 응답 시간 요구사항은 어떻게 되나요?

A) 100ms 이하 (매우 빠름)
B) 500ms 이하 (빠름)
C) 1초 이하 (보통)
D) 2초 이하 (느림)
E) 특별한 요구사항 없음
F) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 7
실시간 주문 모니터링을 위한 통신 방식은?

A) Server-Sent Events (SSE) - 요구사항 문서에 명시됨
B) WebSocket
C) Polling (주기적 요청)
D) Long Polling
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 8
테이블 태블릿의 자동 로그인 정보는 어디에 저장하나요?

A) LocalStorage (브라우저)
B) SessionStorage (브라우저)
C) Cookie
D) IndexedDB (브라우저)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 9
관리자 인증 토큰(JWT)은 어디에 저장하나요?

A) LocalStorage (브라우저)
B) SessionStorage (브라우저)
C) Cookie (HttpOnly)
D) Memory only
E) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## Question 10
메뉴 이미지는 어떻게 관리하나요?

A) 외부 URL만 저장 (이미지는 외부 호스팅)
B) 서버에 업로드 및 저장
C) AWS S3 등 클라우드 스토리지
D) 이미지 기능 제외 (텍스트만)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 11
주문 상태 변경 권한은 누가 가지나요?

A) 관리자만 가능
B) 고객도 취소 가능
C) 주방 직원도 상태 변경 가능
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 12
테이블 세션 만료 정책은 어떻게 되나요?

A) 16시간 고정 (요구사항 문서 명시)
B) 관리자가 수동으로 종료할 때까지
C) 마지막 주문 후 일정 시간 경과 시
D) Other (please describe after [Answer]: tag below)

[Answer]: 

---

## Question 13
장바구니 데이터 유지 기간은?

A) 페이지 새로고침 시에도 유지 (요구사항 명시)
B) 브라우저 닫으면 삭제
C) 일정 시간 후 자동 삭제
D) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Question 14
에러 발생 시 로깅 및 모니터링은 어떻게 하나요?

A) 콘솔 로그만 사용
B) 파일 로깅 (로그 파일 저장)
C) 클라우드 로깅 서비스 (CloudWatch, Stackdriver 등)
D) 로깅 불필요
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 15
개발 환경 설정은 어떻게 관리하나요?

A) .env 파일 사용
B) 환경변수만 사용
C) 설정 파일 (config.json 등)
D) 코드에 하드코딩
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

**모든 질문에 답변하신 후 "완료" 또는 "done"이라고 말씀해주세요.**
