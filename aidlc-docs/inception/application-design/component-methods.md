# Component Methods

이 문서는 각 컴포넌트의 메서드 시그니처를 정의합니다. 상세한 비즈니스 규칙은 Functional Design 단계에서 정의됩니다.

---

## Frontend Component Methods

### Customer App

#### MenuView Component

```typescript
// 메뉴 로드
async loadMenus(): Promise<void>

// 카테고리 변경
onCategoryChange(categoryId: string): void

// 메뉴 상세 보기
showMenuDetail(menuId: string): void

// 장바구니에 추가
addToCart(menuId: string, quantity: number): void
```

---

#### CartView Component

```typescript
// 장바구니 로드
loadCart(): void

// 수량 증가
increaseQuantity(itemId: string): void

// 수량 감소
decreaseQuantity(itemId: string): void

// 아이템 삭제
removeItem(itemId: string): void

// 장바구니 비우기
clearCart(): void

// 주문 확정
async placeOrder(): Promise<void>

// 총 금액 계산
calculateTotal(): number
```

---

#### OrderHistoryView Component

```typescript
// 주문 내역 로드
async loadOrderHistory(): Promise<void>

// 주문 상세 보기
showOrderDetail(orderId: string): void

// 주문 내역 새로고침
async refreshOrders(): Promise<void>
```

---

#### LoginView Component

```typescript
// 로그인 처리
async login(storeId: string, tableNumber: string, password: string): Promise<void>

// 자동 로그인 확인
checkAutoLogin(): boolean

// 로그인 정보 저장
saveLoginInfo(storeId: string, tableNumber: string, token: string): void

// 로그인 정보 로드
loadLoginInfo(): LoginInfo | null
```

---

### Admin App

#### AdminLoginView Component

```typescript
// 관리자 로그인
async login(storeId: string, username: string, password: string): Promise<void>

// JWT 토큰 저장
saveToken(token: string): void

// JWT 토큰 로드
loadToken(): string | null

// 로그인 상태 확인
isLoggedIn(): boolean
```

---

#### OrderDashboardView Component

```typescript
// 주문 대시보드 로드
async loadDashboard(): Promise<void>

// SSE 연결 시작
startSSEConnection(): void

// SSE 연결 종료
stopSSEConnection(): void

// 주문 상태 변경
async updateOrderStatus(orderId: string, status: string): Promise<void>

// 신규 주문 처리 (SSE 이벤트)
onNewOrder(order: Order): void

// 주문 상세 보기
showOrderDetail(orderId: string): void
```

---

#### TableManagementView Component

```typescript
// 테이블 목록 로드
async loadTables(): Promise<void>

// 테이블 초기 설정
async setupTable(tableNumber: string, password: string): Promise<void>

// 주문 삭제
async deleteOrder(orderId: string): Promise<void>

// 테이블 세션 종료
async completeTableSession(tableId: string): Promise<void>

// 과거 주문 내역 조회
async loadOrderHistory(tableId: string, startDate?: Date, endDate?: Date): Promise<void>
```

---

#### MenuManagementView Component

```typescript
// 메뉴 목록 로드
async loadMenus(): Promise<void>

// 메뉴 생성
async createMenu(menuData: MenuCreateDto): Promise<void>

// 메뉴 수정
async updateMenu(menuId: string, menuData: MenuUpdateDto): Promise<void>

// 메뉴 삭제
async deleteMenu(menuId: string): Promise<void>

// 이미지 업로드
async uploadImage(file: File): Promise<string>

// 메뉴 순서 조정
async reorderMenus(menuIds: string[]): Promise<void>
```

---

## Backend Component Methods

### Controller Layer

#### AuthController

```python
# 테이블 로그인
@router.post("/auth/table/login")
async def table_login(request: TableLoginRequest) -> TokenResponse:
    """
    Input: TableLoginRequest (store_id, table_number, password)
    Output: TokenResponse (access_token, token_type)
    """
    pass

# 관리자 로그인
@router.post("/auth/admin/login")
async def admin_login(request: AdminLoginRequest) -> TokenResponse:
    """
    Input: AdminLoginRequest (store_id, username, password)
    Output: TokenResponse (access_token, token_type)
    """
    pass

# 토큰 갱신
@router.post("/auth/refresh")
async def refresh_token(token: str) -> TokenResponse:
    """
    Input: token (str)
    Output: TokenResponse (access_token, token_type)
    """
    pass
```

---

#### MenuController

```python
# 메뉴 목록 조회
@router.get("/menus")
async def get_menus(category_id: Optional[str] = None) -> List[MenuResponse]:
    """
    Input: category_id (Optional[str])
    Output: List[MenuResponse]
    """
    pass

# 메뉴 상세 조회
@router.get("/menus/{menu_id}")
async def get_menu(menu_id: str) -> MenuResponse:
    """
    Input: menu_id (str)
    Output: MenuResponse
    """
    pass

# 메뉴 생성 (관리자)
@router.post("/admin/menus")
async def create_menu(request: MenuCreateRequest) -> MenuResponse:
    """
    Input: MenuCreateRequest (name, price, description, category_id, image_url)
    Output: MenuResponse
    """
    pass

# 메뉴 수정 (관리자)
@router.put("/admin/menus/{menu_id}")
async def update_menu(menu_id: str, request: MenuUpdateRequest) -> MenuResponse:
    """
    Input: menu_id (str), MenuUpdateRequest
    Output: MenuResponse
    """
    pass

# 메뉴 삭제 (관리자)
@router.delete("/admin/menus/{menu_id}")
async def delete_menu(menu_id: str) -> SuccessResponse:
    """
    Input: menu_id (str)
    Output: SuccessResponse
    """
    pass
```

---

#### OrderController

```python
# 주문 생성
@router.post("/orders")
async def create_order(request: OrderCreateRequest) -> OrderResponse:
    """
    Input: OrderCreateRequest (table_id, session_id, items: List[OrderItem])
    Output: OrderResponse
    """
    pass

# 주문 내역 조회 (현재 세션)
@router.get("/orders")
async def get_orders(session_id: str) -> List[OrderResponse]:
    """
    Input: session_id (str)
    Output: List[OrderResponse]
    """
    pass

# 모든 주문 조회 (관리자)
@router.get("/admin/orders")
async def get_all_orders() -> List[OrderResponse]:
    """
    Input: None
    Output: List[OrderResponse]
    """
    pass

# 주문 상태 변경 (관리자)
@router.put("/admin/orders/{order_id}/status")
async def update_order_status(order_id: str, status: OrderStatus) -> OrderResponse:
    """
    Input: order_id (str), status (OrderStatus)
    Output: OrderResponse
    """
    pass

# 주문 삭제 (관리자)
@router.delete("/admin/orders/{order_id}")
async def delete_order(order_id: str) -> SuccessResponse:
    """
    Input: order_id (str)
    Output: SuccessResponse
    """
    pass
```

---

#### TableController

```python
# 테이블 초기 설정 (관리자)
@router.post("/admin/tables/setup")
async def setup_table(request: TableSetupRequest) -> TableResponse:
    """
    Input: TableSetupRequest (table_number, password)
    Output: TableResponse
    """
    pass

# 테이블 세션 종료 (관리자)
@router.post("/admin/tables/{table_id}/complete")
async def complete_table_session(table_id: str) -> SuccessResponse:
    """
    Input: table_id (str)
    Output: SuccessResponse
    """
    pass

# 과거 주문 내역 조회 (관리자)
@router.get("/admin/tables/{table_id}/history")
async def get_table_history(
    table_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[OrderHistoryResponse]:
    """
    Input: table_id (str), start_date (Optional[datetime]), end_date (Optional[datetime])
    Output: List[OrderHistoryResponse]
    """
    pass
```

---

#### SSEController

```python
# SSE 연결 (관리자)
@router.get("/admin/orders/stream")
async def order_stream(request: Request) -> EventSourceResponse:
    """
    Input: Request
    Output: EventSourceResponse (SSE stream)
    """
    pass
```

---

### Service Layer

#### AuthService

```python
class AuthService:
    def __init__(self, user_repository: UserRepository, table_repository: TableRepository):
        self.user_repository = user_repository
        self.table_repository = table_repository
    
    # 테이블 로그인 검증
    async def authenticate_table(self, store_id: str, table_number: str, password: str) -> str:
        """
        Input: store_id, table_number, password
        Output: JWT token (str)
        Business Logic: 테이블 정보 검증, 세션 생성, JWT 발급
        """
        pass
    
    # 관리자 로그인 검증
    async def authenticate_admin(self, store_id: str, username: str, password: str) -> str:
        """
        Input: store_id, username, password
        Output: JWT token (str)
        Business Logic: 관리자 정보 검증, 비밀번호 확인, JWT 발급
        """
        pass
    
    # JWT 토큰 생성
    def create_jwt_token(self, user_id: str, role: str, expires_hours: int = 16) -> str:
        """
        Input: user_id, role, expires_hours
        Output: JWT token (str)
        Business Logic: JWT 토큰 생성 (16시간 만료)
        """
        pass
    
    # JWT 토큰 검증
    def verify_jwt_token(self, token: str) -> dict:
        """
        Input: token (str)
        Output: Decoded token payload (dict)
        Business Logic: JWT 토큰 검증 및 디코딩
        """
        pass
    
    # 비밀번호 해싱
    def hash_password(self, password: str) -> str:
        """
        Input: password (str)
        Output: Hashed password (str)
        Business Logic: bcrypt 해싱
        """
        pass
    
    # 비밀번호 검증
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Input: plain_password, hashed_password
        Output: bool
        Business Logic: bcrypt 검증
        """
        pass
```

---

#### MenuService

```python
class MenuService:
    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository
    
    # 메뉴 목록 조회
    async def get_menus(self, category_id: Optional[str] = None) -> List[Menu]:
        """
        Input: category_id (Optional)
        Output: List[Menu]
        Business Logic: 카테고리별 메뉴 조회, 노출 순서대로 정렬
        """
        pass
    
    # 메뉴 상세 조회
    async def get_menu_by_id(self, menu_id: str) -> Menu:
        """
        Input: menu_id
        Output: Menu
        Business Logic: 메뉴 ID로 조회
        """
        pass
    
    # 메뉴 생성
    async def create_menu(self, menu_data: MenuCreateDto) -> Menu:
        """
        Input: MenuCreateDto
        Output: Menu
        Business Logic: 메뉴 검증, 생성
        """
        pass
    
    # 메뉴 수정
    async def update_menu(self, menu_id: str, menu_data: MenuUpdateDto) -> Menu:
        """
        Input: menu_id, MenuUpdateDto
        Output: Menu
        Business Logic: 메뉴 검증, 수정
        """
        pass
    
    # 메뉴 삭제
    async def delete_menu(self, menu_id: str) -> bool:
        """
        Input: menu_id
        Output: bool
        Business Logic: 메뉴 삭제
        """
        pass
    
    # 이미지 업로드 처리
    async def upload_image(self, file: UploadFile) -> str:
        """
        Input: UploadFile
        Output: Image URL (str)
        Business Logic: 이미지 저장, URL 반환
        """
        pass
```

---

#### OrderService

```python
class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        menu_repository: MenuRepository,
        sse_service: SSEService
    ):
        self.order_repository = order_repository
        self.menu_repository = menu_repository
        self.sse_service = sse_service
    
    # 주문 생성
    async def create_order(self, order_data: OrderCreateDto) -> Order:
        """
        Input: OrderCreateDto (table_id, session_id, items)
        Output: Order
        Business Logic: 주문 검증, 금액 계산, 주문 생성, SSE 알림
        """
        pass
    
    # 주문 내역 조회 (현재 세션)
    async def get_orders_by_session(self, session_id: str) -> List[Order]:
        """
        Input: session_id
        Output: List[Order]
        Business Logic: 세션 ID로 주문 조회, 시간 순 정렬
        """
        pass
    
    # 모든 주문 조회 (관리자)
    async def get_all_orders(self) -> List[Order]:
        """
        Input: None
        Output: List[Order]
        Business Logic: 모든 주문 조회, 테이블별 그룹화
        """
        pass
    
    # 주문 상태 변경
    async def update_order_status(self, order_id: str, status: OrderStatus) -> Order:
        """
        Input: order_id, status
        Output: Order
        Business Logic: 주문 상태 업데이트, SSE 알림
        """
        pass
    
    # 주문 삭제
    async def delete_order(self, order_id: str) -> bool:
        """
        Input: order_id
        Output: bool
        Business Logic: 주문 삭제, 테이블 총 주문액 재계산
        """
        pass
    
    # 주문 금액 계산
    def calculate_order_total(self, items: List[OrderItem]) -> Decimal:
        """
        Input: List[OrderItem]
        Output: Decimal (총 금액)
        Business Logic: 각 아이템 금액 합산
        """
        pass
```

---

#### TableService

```python
class TableService:
    def __init__(
        self,
        table_repository: TableRepository,
        order_repository: OrderRepository
    ):
        self.table_repository = table_repository
        self.order_repository = order_repository
    
    # 테이블 초기 설정
    async def setup_table(self, table_number: str, password: str) -> Table:
        """
        Input: table_number, password
        Output: Table
        Business Logic: 테이블 생성/업데이트, 비밀번호 해싱, 세션 생성
        """
        pass
    
    # 테이블 세션 종료
    async def complete_table_session(self, table_id: str) -> bool:
        """
        Input: table_id
        Output: bool
        Business Logic: 주문 내역 이력으로 이동, 테이블 리셋
        """
        pass
    
    # 테이블 세션 만료 확인
    def is_session_expired(self, table: Table) -> bool:
        """
        Input: Table
        Output: bool
        Business Logic: 16시간 OR 마지막 주문 후 일정 시간 확인
        """
        pass
    
    # 과거 주문 내역 조회
    async def get_table_history(
        self,
        table_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[OrderHistory]:
        """
        Input: table_id, start_date, end_date
        Output: List[OrderHistory]
        Business Logic: 테이블 과거 주문 조회, 날짜 필터링
        """
        pass
```

---

#### SSEService

```python
class SSEService:
    def __init__(self):
        self.connections: Dict[str, asyncio.Queue] = {}
    
    # 클라이언트 연결 추가
    def add_connection(self, client_id: str) -> asyncio.Queue:
        """
        Input: client_id
        Output: asyncio.Queue
        Business Logic: 새 연결 추가, 큐 생성
        """
        pass
    
    # 클라이언트 연결 제거
    def remove_connection(self, client_id: str) -> None:
        """
        Input: client_id
        Output: None
        Business Logic: 연결 제거
        """
        pass
    
    # 이벤트 브로드캐스트
    async def broadcast(self, event_type: str, data: dict) -> None:
        """
        Input: event_type, data
        Output: None
        Business Logic: 모든 연결된 클라이언트에 이벤트 전송
        """
        pass
    
    # 특정 클라이언트에 이벤트 전송
    async def send_to_client(self, client_id: str, event_type: str, data: dict) -> None:
        """
        Input: client_id, event_type, data
        Output: None
        Business Logic: 특정 클라이언트에 이벤트 전송
        """
        pass
```

---

### Repository Layer

#### UserRepository

```python
class UserRepository:
    def __init__(self, db_session: Session):
        self.db = db_session
    
    # 사용자 조회 (username)
    async def get_by_username(self, store_id: str, username: str) -> Optional[User]:
        """
        Input: store_id, username
        Output: Optional[User]
        """
        pass
    
    # 사용자 조회 (ID)
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """
        Input: user_id
        Output: Optional[User]
        """
        pass
    
    # 사용자 생성
    async def create(self, user_data: UserCreateDto) -> User:
        """
        Input: UserCreateDto
        Output: User
        """
        pass
```

---

#### TableRepository

```python
class TableRepository:
    def __init__(self, db_session: Session):
        self.db = db_session
    
    # 테이블 조회 (table_number)
    async def get_by_table_number(self, store_id: str, table_number: str) -> Optional[Table]:
        """
        Input: store_id, table_number
        Output: Optional[Table]
        """
        pass
    
    # 테이블 조회 (ID)
    async def get_by_id(self, table_id: str) -> Optional[Table]:
        """
        Input: table_id
        Output: Optional[Table]
        """
        pass
    
    # 테이블 생성
    async def create(self, table_data: TableCreateDto) -> Table:
        """
        Input: TableCreateDto
        Output: Table
        """
        pass
    
    # 테이블 업데이트
    async def update(self, table_id: str, table_data: TableUpdateDto) -> Table:
        """
        Input: table_id, TableUpdateDto
        Output: Table
        """
        pass
    
    # 모든 테이블 조회
    async def get_all(self, store_id: str) -> List[Table]:
        """
        Input: store_id
        Output: List[Table]
        """
        pass
```

---

#### MenuRepository

```python
class MenuRepository:
    def __init__(self, db_session: Session):
        self.db = db_session
    
    # 메뉴 목록 조회
    async def get_all(self, store_id: str, category_id: Optional[str] = None) -> List[Menu]:
        """
        Input: store_id, category_id (Optional)
        Output: List[Menu]
        """
        pass
    
    # 메뉴 조회 (ID)
    async def get_by_id(self, menu_id: str) -> Optional[Menu]:
        """
        Input: menu_id
        Output: Optional[Menu]
        """
        pass
    
    # 메뉴 생성
    async def create(self, menu_data: MenuCreateDto) -> Menu:
        """
        Input: MenuCreateDto
        Output: Menu
        """
        pass
    
    # 메뉴 업데이트
    async def update(self, menu_id: str, menu_data: MenuUpdateDto) -> Menu:
        """
        Input: menu_id, MenuUpdateDto
        Output: Menu
        """
        pass
    
    # 메뉴 삭제
    async def delete(self, menu_id: str) -> bool:
        """
        Input: menu_id
        Output: bool
        """
        pass
```

---

#### OrderRepository

```python
class OrderRepository:
    def __init__(self, db_session: Session):
        self.db = db_session
    
    # 주문 생성
    async def create(self, order_data: OrderCreateDto) -> Order:
        """
        Input: OrderCreateDto
        Output: Order
        """
        pass
    
    # 주문 조회 (ID)
    async def get_by_id(self, order_id: str) -> Optional[Order]:
        """
        Input: order_id
        Output: Optional[Order]
        """
        pass
    
    # 세션별 주문 조회
    async def get_by_session(self, session_id: str) -> List[Order]:
        """
        Input: session_id
        Output: List[Order]
        """
        pass
    
    # 모든 주문 조회
    async def get_all(self, store_id: str) -> List[Order]:
        """
        Input: store_id
        Output: List[Order]
        """
        pass
    
    # 주문 업데이트
    async def update(self, order_id: str, order_data: OrderUpdateDto) -> Order:
        """
        Input: order_id, OrderUpdateDto
        Output: Order
        """
        pass
    
    # 주문 삭제
    async def delete(self, order_id: str) -> bool:
        """
        Input: order_id
        Output: bool
        """
        pass
    
    # 주문 이력으로 이동
    async def move_to_history(self, session_id: str) -> bool:
        """
        Input: session_id
        Output: bool
        """
        pass
```

---

## Method Summary

### Frontend
- **Customer App**: 약 30개 메서드
- **Admin App**: 약 35개 메서드
- **Shared**: 약 10개 메서드

### Backend
- **Controller Layer**: 약 20개 엔드포인트
- **Service Layer**: 약 30개 메서드
- **Repository Layer**: 약 25개 메서드

**총 메서드 수**: 약 150개

**Note**: 상세한 비즈니스 규칙 및 구현 로직은 Functional Design 단계에서 정의됩니다.

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
