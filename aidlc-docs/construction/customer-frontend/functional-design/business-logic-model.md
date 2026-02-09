# Business Logic Model - Customer Frontend

## Overview

Customer Frontend의 비즈니스 로직은 5개의 주요 워크플로우로 구성됩니다. 각 워크플로우는 User Story에 대응됩니다.

---

## Workflow 1: 테이블 자동 로그인 (Story 1.1)

### 목적
테이블 태블릿의 초기 설정 및 자동 로그인을 처리합니다.

### 시나리오

#### 1.1.1 초기 설정 (First-time Setup)

**Trigger**: 앱 시작 시 LocalStorage에 세션 정보 없음

**Steps**:
1. 로그인 화면 표시
2. 사용자 입력 수집:
   - 매장 ID (또는 매장 선택)
   - 테이블 번호
   - 비밀번호
3. 입력 검증:
   - 모든 필드 필수
   - 테이블 번호 형식 확인
4. Backend API 호출: `POST /api/auth/table-login`
5. 응답 처리:
   - **성공**: TableSession 생성 및 LocalStorage 저장
   - **실패**: 에러 메시지 표시
6. 메뉴 화면으로 이동

**Business Rules**:
- 테이블 번호는 대소문자 구분 없음
- 비밀번호는 최소 4자 이상
- 로그인 실패 시 5회 제한 (Backend에서 처리)

---

#### 1.1.2 자동 로그인 (Auto Login)

**Trigger**: 앱 시작 시 LocalStorage에 세션 정보 존재

**Steps**:
1. LocalStorage에서 TableSession 로드
2. 세션 유효성 검증:
   - `expiresAt` > 현재 시각
   - `sessionToken` 존재
3. 세션 유효:
   - 메뉴 화면으로 자동 이동
   - 헤더에 테이블 정보 표시
4. 세션 만료:
   - LocalStorage 정리
   - 로그인 화면 표시
   - 알림: "세션이 만료되었습니다"

**Business Rules**:
- 세션 만료 시간: 16시간 OR 마지막 주문 후 2시간 (Backend 관리)
- 클라이언트는 `expiresAt`만 체크

---

### Data Flow

```
[User Input] → [Validation] → [API Call] → [TableSession] → [LocalStorage]
                                                ↓
                                          [Menu Screen]
```

---

## Workflow 2: 메뉴 조회 및 탐색 (Story 1.2)

### 목적
메뉴 목록을 조회하고 카테고리별로 탐색합니다.

### 시나리오

#### 2.1 메뉴 로딩

**Trigger**: 메뉴 화면 진입

**Steps**:
1. 로딩 스피너 표시
2. Backend API 호출: `GET /api/menus?store_id={storeId}`
3. 응답 처리:
   - **성공**: Menu[] 및 Category[] 파싱
   - **실패**: 에러 메시지 표시 + 재시도 버튼
4. Pinia Store에 저장 (`menuStore`)
5. 카테고리별로 메뉴 그룹화
6. 첫 번째 카테고리 선택 (기본)
7. 메뉴 카드 렌더링

**Business Rules**:
- `isAvailable: false` 메뉴는 비활성화 표시 (선택 불가)
- 메뉴는 `displayOrder` 순으로 정렬
- 카테고리는 `displayOrder` 순으로 정렬

---

#### 2.2 카테고리 전환

**Trigger**: 사용자가 카테고리 탭 클릭

**Steps**:
1. 선택된 카테고리 ID 저장
2. 해당 카테고리의 메뉴만 필터링
3. 메뉴 카드 재렌더링
4. 탭 UI 업데이트 (선택된 탭 강조)

**Business Rules**:
- 카테고리 전환 시 스크롤 위치 초기화

---

#### 2.3 메뉴 상세 보기

**Trigger**: 사용자가 메뉴 카드 클릭

**Steps**:
1. 메뉴 상세 모달 표시
2. 메뉴 정보 표시:
   - 이미지 (큰 사이즈)
   - 메뉴명
   - 설명
   - 가격
3. "장바구니 담기" 버튼 표시
4. 수량 선택 UI (기본 1개)

**Business Rules**:
- `isAvailable: false` 메뉴는 "품절" 표시 + 버튼 비활성화

---

#### 2.4 이미지 로딩 실패 처리

**Trigger**: 메뉴 이미지 로딩 실패

**Steps**:
1. `<img>` 태그의 `onerror` 이벤트 감지
2. 기본 이미지로 대체 (`/images/placeholder.png`)
3. 이미지 영역에 "이미지 없음" 텍스트 표시 (선택사항)

**Business Rules**:
- 기본 이미지는 로컬 assets에 포함

---

### Data Flow

```
[API Call] → [Menu[] + Category[]] → [Pinia Store] → [UI Rendering]
                                            ↓
                                    [Category Filter]
                                            ↓
                                    [Menu Cards]
```

---

## Workflow 3: 장바구니 관리 (Story 1.3)

### 목적
장바구니에 메뉴를 추가하고 수량을 조절합니다.

### 시나리오

#### 3.1 장바구니에 추가

**Trigger**: 메뉴 상세 모달에서 "장바구니 담기" 클릭

**Steps**:
1. 선택된 메뉴 정보 수집:
   - menuId, menuName, price, quantity, imageUrl
2. 장바구니에 동일 메뉴 존재 확인:
   - **존재**: 수량만 증가
   - **없음**: 새 CartItem 추가
3. `subtotal` 계산: `price × quantity`
4. Pinia Store 업데이트 (`cartStore`)
5. LocalStorage 즉시 저장
6. 토스트 메시지: "장바구니에 추가되었습니다"
7. 모달 닫기

**Business Rules**:
- 동일 메뉴는 하나의 CartItem으로 관리 (수량만 증가)
- 최대 수량 제한 없음

---

#### 3.2 수량 증가/감소

**Trigger**: 장바구니 화면에서 +/- 버튼 클릭

**Steps**:
1. 버튼 종류 확인 (증가/감소)
2. 수량 업데이트:
   - **증가**: `quantity += 1`
   - **감소**: `quantity -= 1`
3. 수량 검증:
   - `quantity < 1`: CartItem 삭제
   - `quantity >= 1`: `subtotal` 재계산
4. Pinia Store 업데이트
5. LocalStorage 즉시 저장
6. 총 금액 재계산

**Business Rules**:
- 수량 0이 되면 자동 삭제 (확인 없음)
- 수량 증가 시 최대 제한 없음

---

#### 3.3 아이템 삭제

**Trigger**: 장바구니 화면에서 "삭제" 버튼 클릭

**Steps**:
1. 해당 CartItem 제거
2. Pinia Store 업데이트
3. LocalStorage 즉시 저장
4. 총 금액 재계산
5. 장바구니 비어있으면 "장바구니가 비어있습니다" 메시지 표시

**Business Rules**:
- 삭제 시 확인 팝업 없음 (빠른 UX)

---

#### 3.4 장바구니 비우기

**Trigger**: 장바구니 화면에서 "전체 삭제" 버튼 클릭

**Steps**:
1. 확인 팝업 표시: "장바구니를 비우시겠습니까?"
2. 사용자 확인:
   - **예**: 모든 CartItem 삭제
   - **아니오**: 취소
3. Pinia Store 업데이트
4. LocalStorage 즉시 저장
5. "장바구니가 비어있습니다" 메시지 표시

**Business Rules**:
- 전체 삭제는 확인 팝업 필수

---

#### 3.5 총 금액 계산

**Trigger**: 장바구니 변경 시 (추가/수량 변경/삭제)

**Steps**:
1. 모든 CartItem의 `subtotal` 합산
2. `totalAmount` 업데이트
3. `itemCount` 계산 (모든 quantity 합산)
4. UI 업데이트 (헤더 배지, 장바구니 화면)

**Calculation**:
```javascript
totalAmount = items.reduce((sum, item) => sum + item.subtotal, 0)
itemCount = items.reduce((sum, item) => sum + item.quantity, 0)
```

---

### Data Flow

```
[Menu] → [Add to Cart] → [CartItem] → [Cart] → [LocalStorage]
                              ↓
                        [Quantity +/-]
                              ↓
                        [Subtotal Calc]
                              ↓
                        [Total Amount]
```

---

## Workflow 4: 주문 생성 (Story 1.4)

### 목적
장바구니 내용을 주문으로 생성합니다.

### 시나리오

#### 4.1 주문 확정 전 확인

**Trigger**: 장바구니 화면에서 "주문하기" 버튼 클릭

**Steps**:
1. 장바구니 비어있는지 확인:
   - **비어있음**: "장바구니가 비어있습니다" 알림
   - **있음**: 다음 단계 진행
2. 주문 확인 모달 표시:
   - 주문 아이템 목록
   - 총 금액
   - "확인" / "취소" 버튼
3. 사용자 선택 대기

**Business Rules**:
- 장바구니 비어있으면 주문 불가

---

#### 4.2 주문 생성 API 호출

**Trigger**: 주문 확인 모달에서 "확인" 클릭

**Steps**:
1. 로딩 스피너 표시
2. 주문 데이터 준비:
   ```javascript
   {
     storeId: session.storeId,
     tableNumber: session.tableNumber,
     sessionToken: session.sessionToken,
     items: cart.items.map(item => ({
       menuId: item.menuId,
       quantity: item.quantity
     })),
     totalAmount: cart.totalAmount
   }
   ```
3. Backend API 호출: `POST /api/orders`
4. 응답 처리:
   - **성공**: 다음 단계 진행
   - **실패**: 에러 처리 (4.4 참조)

**Business Rules**:
- `sessionToken`은 Header에 포함 (`X-Session-Token`)

---

#### 4.3 주문 성공 처리

**Trigger**: 주문 생성 API 성공 응답

**Steps**:
1. 주문 번호 추출 (`orderNumber`)
2. 장바구니 비우기:
   - Pinia Store 초기화
   - LocalStorage 삭제
3. 토스트 메시지 표시:
   - "주문이 완료되었습니다"
   - 주문 번호 표시 (2초)
4. 자동으로 메뉴 화면으로 이동
5. 주문 확인 모달 닫기

**Business Rules**:
- 주문 성공 시 장바구니 자동 비우기
- 2초 후 자동 이동

---

#### 4.4 주문 실패 처리

**Trigger**: 주문 생성 API 실패 응답

**Steps**:
1. 에러 타입 확인:
   - **401 Unauthorized**: 세션 만료
   - **400 Bad Request**: 입력 오류
   - **500 Server Error**: 서버 오류
   - **Network Error**: 네트워크 오류
2. 에러 메시지 표시:
   - **세션 만료**: "세션이 만료되었습니다. 다시 로그인해주세요"
   - **입력 오류**: Backend 에러 메시지 표시
   - **서버 오류**: "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요"
   - **네트워크 오류**: "네트워크 연결을 확인해주세요"
3. 장바구니 유지 (삭제하지 않음)
4. 재시도 옵션 제공:
   - **세션 만료**: 로그인 화면으로 이동
   - **기타**: "다시 시도" 버튼

**Business Rules**:
- 주문 실패 시 장바구니 유지
- 네트워크 에러는 자동 재시도 1회

---

### Data Flow

```
[Cart] → [Order Confirmation] → [API Call] → [Success/Failure]
                                                    ↓
                                            [Clear Cart]
                                                    ↓
                                            [Menu Screen]
```

---

## Workflow 5: 주문 내역 조회 (Story 1.5)

### 목적
현재 테이블 세션의 주문 내역을 조회합니다.

### 시나리오

#### 5.1 주문 내역 로딩

**Trigger**: 주문 내역 화면 진입

**Steps**:
1. 로딩 스피너 표시
2. Backend API 호출: `GET /api/orders`
   - Header: `X-Session-Token: {sessionToken}`
3. 응답 처리:
   - **성공**: Order[] 파싱
   - **실패**: 에러 메시지 표시
4. Pinia Store에 저장 (`orderStore`)
5. 주문 목록 렌더링 (최신순)

**Business Rules**:
- 현재 세션의 주문만 반환 (Backend 필터링)
- 최신순 정렬 (`createdAt DESC`)

---

#### 5.2 주문 상태 표시

**Trigger**: 주문 목록 렌더링

**Steps**:
1. 각 주문의 `status` 확인
2. 상태별 UI 표시:
   - **대기중**: 노란색 배지
   - **준비중**: 파란색 배지
   - **완료**: 초록색 배지
3. 상태별 아이콘 표시 (선택사항)

**Business Rules**:
- 상태는 Backend에서 관리 (Frontend는 표시만)

---

#### 5.3 주문 상세 보기

**Trigger**: 주문 카드 클릭

**Steps**:
1. 주문 상세 모달 표시
2. 주문 정보 표시:
   - 주문 번호
   - 주문 시각
   - 주문 아이템 목록 (메뉴명, 수량, 가격)
   - 총 금액
   - 주문 상태
3. "닫기" 버튼

**Business Rules**:
- 주문 수정/취소 기능 없음 (고객용 앱)

---

#### 5.4 빈 주문 내역 처리

**Trigger**: 주문 내역이 비어있음

**Steps**:
1. "주문 내역이 없습니다" 메시지 표시
2. "메뉴 보러가기" 버튼 표시
3. 버튼 클릭 시 메뉴 화면으로 이동

**Business Rules**:
- 첫 주문 전에는 항상 빈 상태

---

### Data Flow

```
[API Call] → [Order[]] → [Pinia Store] → [UI Rendering]
                              ↓
                        [Status Display]
                              ↓
                        [Order Detail]
```

---

## Cross-Workflow Logic

### 세션 만료 처리 (Global)

**Trigger**: 모든 API 호출 시 401 Unauthorized 응답

**Steps**:
1. 401 에러 감지 (Axios Interceptor)
2. LocalStorage 정리:
   - `table_session` 삭제
   - `cart_items` 삭제
3. Pinia Store 초기화:
   - `authStore` 초기화
   - `cartStore` 초기화
   - `orderStore` 초기화
4. 알림 모달 표시: "세션이 만료되었습니다"
5. 로그인 화면으로 강제 이동

**Business Rules**:
- 세션 만료 시 모든 데이터 초기화
- 장바구니 데이터도 삭제 (보안)

---

### 네트워크 에러 처리 (Global)

**Trigger**: API 호출 시 네트워크 에러

**Steps**:
1. 네트워크 에러 감지 (Axios Interceptor)
2. 자동 재시도 (1회):
   - 1초 대기 후 재시도
3. 재시도 실패:
   - 에러 메시지 표시: "네트워크 연결을 확인해주세요"
   - "다시 시도" 버튼 표시

**Business Rules**:
- 자동 재시도는 1회만
- 사용자가 수동으로 추가 재시도 가능

---

## State Management (Pinia Stores)

### authStore
- **State**: `session` (TableSession | null)
- **Actions**: `login()`, `logout()`, `checkSession()`

### menuStore
- **State**: `menus` (Menu[]), `categories` (Category[]), `selectedCategoryId` (number)
- **Actions**: `loadMenus()`, `selectCategory(id)`

### cartStore
- **State**: `items` (CartItem[]), `totalAmount` (number), `itemCount` (number)
- **Actions**: `addItem()`, `updateQuantity()`, `removeItem()`, `clear()`
- **Getters**: `totalAmount`, `itemCount`

### orderStore
- **State**: `orders` (Order[])
- **Actions**: `createOrder()`, `loadOrders()`

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
