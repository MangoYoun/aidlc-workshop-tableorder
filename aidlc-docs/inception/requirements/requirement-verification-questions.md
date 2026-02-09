# Requirements Clarification Questions

답변을 분석한 결과, 요구사항 문서와 충돌하는 부분이 발견되어 명확화가 필요합니다.

---

## Contradiction 1: 테이블 태블릿 로그인 정보 저장 방식

**발견된 모순:**
- Q8에서 **SessionStorage** 선택 (B)
- 요구사항 문서: "1회 로그인 성공 후, 저장된 정보로 **자동 로그인**"
- 요구사항 문서: "**16시간 세션** 유지"

**문제점:** SessionStorage는 브라우저 탭을 닫으면 데이터가 삭제되므로, 태블릿을 재시작하거나 브라우저를 닫았다가 다시 열면 자동 로그인이 불가능합니다.

### Clarification Question 1
테이블 태블릿의 자동 로그인 정보 저장 방식을 다시 선택해주세요.

A) LocalStorage - 브라우저를 닫아도 유지, 자동 로그인 가능
B) SessionStorage - 브라우저 탭 닫으면 삭제, 매번 수동 로그인 필요
C) Cookie (with expiration) - 브라우저를 닫아도 유지, 자동 로그인 가능
D) Other (please describe after [Answer]: tag below)

[Answer]: A 

---

## Contradiction 2: 관리자 JWT 토큰 저장 방식

**발견된 모순:**
- Q9에서 **Memory only** 선택 (D)
- 요구사항 문서: "**브라우저 새로고침 시 세션 유지**"
- 요구사항 문서: "**16시간 세션** 유지"

**문제점:** Memory only는 페이지 새로고침 시 데이터가 삭제되므로, 새로고침할 때마다 다시 로그인해야 합니다.

### Clarification Question 2
관리자 JWT 토큰 저장 방식을 다시 선택해주세요.

A) LocalStorage - 새로고침 시에도 유지, 16시간 세션 가능
B) SessionStorage - 새로고침 시에도 유지 (탭 닫으면 삭제)
C) Cookie (HttpOnly) - 새로고침 시에도 유지, 보안성 높음
D) Memory only - 새로고침 시 삭제, 매번 로그인 필요
E) Other (please describe after [Answer]: tag below)

[Answer]: A 

---

## Ambiguity 1: 테이블 세션 만료 정책

**발견된 애매함:**
- Q12에서 "마지막 주문 후 일정 시간 경과 시" 선택 (C)
- 요구사항 문서: "**16시간 세션** 유지"

**질문:** 두 정책을 모두 적용하시겠습니까, 아니면 하나만 적용하시겠습니까?

### Clarification Question 3
테이블 세션 만료 정책을 명확히 해주세요.

A) 16시간 고정 만료 (로그인 시점부터 16시간 후 자동 만료)
B) 마지막 주문 후 일정 시간 경과 시 만료 (예: 2시간 동안 주문 없으면 만료)
C) 둘 다 적용 (16시간 고정 OR 마지막 주문 후 일정 시간, 둘 중 먼저 도달하는 조건)
D) 관리자가 수동으로 "매장 이용 완료" 처리할 때까지 유지
E) Other (please describe after [Answer]: tag below)

[Answer]: C

**Note**: 사용자 요청에 따라 테이블 세션 만료 정책 적용
- 16시간 고정 만료 (테이블 태블릿 로그인 세션)
- 마지막 주문 후 일정 시간 경과 시 만료 (고객 식사 세션)
- 둘 중 먼저 도달하는 조건으로 세션 종료 

---

## Ambiguity 2: 장바구니 데이터 유지 기간

**발견된 애매함:**
- Q13에서 "일정 시간 후 자동 삭제" 선택 (C)
- 요구사항 문서: "**페이지 새로고침 시에도 유지**"

**질문:** 장바구니 데이터의 정확한 유지 정책은 무엇인가요?

### Clarification Question 4
장바구니 데이터 유지 정책을 명확히 해주세요.

A) 페이지 새로고침 시에도 유지, 주문 완료 시에만 삭제
B) 페이지 새로고침 시에도 유지, 일정 시간(예: 30분) 후 자동 삭제
C) 페이지 새로고침 시에도 유지, 테이블 세션 종료 시 삭제
D) SessionStorage 사용, 브라우저 탭 닫으면 삭제
E) Other (please describe after [Answer]: tag below)

[Answer]: C 

---

**모든 질문에 답변하신 후 "완료" 또는 "done"이라고 말씀해주세요.**
