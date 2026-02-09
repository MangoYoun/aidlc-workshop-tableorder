# Contract/Interface Definition for Backend Service

## Unit Context

**Unit**: Backend Service  
**Workspace Root**: Workspace root (Greenfield single unit)  
**Project Structure**: `src/`, `tests/`, `config/` in workspace root

**Stories Implemented**:
- Story 3.1: 성능 요구사항
- Story 3.2: 보안 요구사항
- Story 3.3: 가용성 요구사항

**Dependencies**: None (독립적 Unit)

**Database Entities Owned**:
- Store, AdminUser, TableAuth, TableSession
- Category, Menu, Order, OrderItem

**Service Boundaries**:
- 인증 및 권한 관리
- 메뉴 관리
- 주문 관리
- 테이블 세션 관리
- 실시간 통신 (SSE)

---

## 1. Models Layer (Database Entities)

### Store
```python
class Store(Base):
    """매장 엔티티"""
    __tablename__ = "stores"
    
    id: int  # Primary Key
    name: str  # 매장 이름
    created_at: datetime
    updated_at: datetime
```

### AdminUser
```python
class AdminUser(Base):
    """관리자 사용자 엔티티"""
    __tablename__ = "admin_users"
    
    id: int  # Primary Key
    store_id: int  # Foreign Key
    username: str
    password_hash: str
    failed_login_attempts: int
    locked_until: Optional[datetime]
    created_at: datetime
    updated_at: datetime
```

### TableAuth
```python
class TableAuth(Base):
    """테이블 인증 엔티티"""
    __tablename__ = "table_auths"
    
    id: int  # Primary Key
    store_id: int  # Foreign Key
    table_number: str
    password_hash: str
    failed_login_attempts: int
    locked_until: Optional[datetime]
    created_at: datetime
    updated_at: datetime
```

### TableSession
```python
class TableSession(Base):
    """테이블 세션 엔티티"""
    __tablename__ = "table_sessions"
    
    id: int  # Primary Key
    table_auth_id: int  # Foreign Key
    session_token: str
    created_at: datetime
    last_order_at: Optional[datetime]
    expired_at: Optional[datetime]
    closed_at: Optional[datetime]
    is_active: bool
```


### Category, Menu, Order, OrderItem
```python
class Category(Base):
    """메뉴 카테고리 엔티티"""
    __tablename__ = "categories"
    id: int
    store_id: int
    name: str
    display_order: int
    created_at: datetime
    updated_at: datetime

class Menu(Base):
    """메뉴 엔티티"""
    __tablename__ = "menus"
    id: int
    store_id: int
    category_id: int
    name: str
    description: Optional[str]
    price: int
    image_url: Optional[str]
    display_order: int
    is_available: bool
    created_at: datetime
    updated_at: datetime

class Order(Base):
    """주문 엔티티"""
    __tablename__ = "orders"
    id: int
    store_id: int
    table_session_id: int
    order_number: str
    total_amount: int
    status: str  # "pending", "preparing", "completed"
    created_at: datetime
    updated_at: datetime

class OrderItem(Base):
    """주문 아이템 엔티티"""
    __tablename__ = "order_items"
    id: int
    order_id: int
    menu_id: int
    menu_name: str
    menu_price: int
    quantity: int
    subtotal: int
    created_at: datetime
```

---

## 2. Repository Layer

### AdminUserRepository
```python
class AdminUserRepository:
    """관리자 사용자 Repository"""
    
    def find_by_store_and_username(store_id: int, username: str) -> Optional[AdminUser]:
        """매장 ID와 사용자명으로 관리자 조회"""
        pass
    
    def save(admin_user: AdminUser) -> AdminUser:
        """관리자 저장"""
        pass
    
    def update_login_attempts(admin_user_id: int, attempts: int, locked_until: Optional[datetime]) -> None:
        """로그인 시도 횟수 업데이트"""
        pass
```

### TableAuthRepository
```python
class TableAuthRepository:
    """테이블 인증 Repository"""
    
    def find_by_store_and_table_number(store_id: int, table_number: str) -> Optional[TableAuth]:
        """매장 ID와 테이블 번호로 테이블 인증 조회"""
        pass
    
    def save(table_auth: TableAuth) -> TableAuth:
        """테이블 인증 저장"""
        pass
    
    def update_login_attempts(table_auth_id: int, attempts: int, locked_until: Optional[datetime]) -> None:
        """로그인 시도 횟수 업데이트"""
        pass
```

### TableSessionRepository
```python
class TableSessionRepository:
    """테이블 세션 Repository"""
    
    def find_by_token(session_token: str) -> Optional[TableSession]:
        """세션 토큰으로 세션 조회"""
        pass
    
    def find_active_by_table_auth(table_auth_id: int) -> Optional[TableSession]:
        """테이블 인증 ID로 활성 세션 조회"""
        pass
    
    def save(session: TableSession) -> TableSession:
        """세션 저장"""
        pass
    
    def update_last_order_time(session_id: int, last_order_at: datetime) -> None:
        """마지막 주문 시간 업데이트"""
        pass
    
    def close_session(session_id: int, closed_at: datetime) -> None:
        """세션 종료"""
        pass
```

### MenuRepository, OrderRepository
```python
class MenuRepository:
    """메뉴 Repository"""
    def find_by_store(store_id: int) -> List[Menu]:
        pass
    def find_by_id(menu_id: int) -> Optional[Menu]:
        pass
    def save(menu: Menu) -> Menu:
        pass
    def delete(menu_id: int) -> None:
        pass

class OrderRepository:
    """주문 Repository"""
    def find_by_session(session_id: int) -> List[Order]:
        pass
    def find_by_store_and_status(store_id: int, status: str) -> List[Order]:
        pass
    def save(order: Order) -> Order:
        pass
    def update_status(order_id: int, status: str) -> None:
        pass
```

---

## 3. Service Layer (Business Logic)

### AuthService
```python
class AuthService:
    """인증 서비스"""
    
    def login_admin(store_id: int, username: str, password: str) -> str:
        """관리자 로그인
        Args:
            store_id: 매장 ID
            username: 사용자명
            password: 비밀번호
        Returns:
            JWT 토큰
        Raises:
            AuthenticationError: 인증 실패
            AccountLockedError: 계정 잠금
        """
        pass
    
    def login_table(store_id: int, table_number: str, password: str) -> str:
        """테이블 로그인
        Args:
            store_id: 매장 ID
            table_number: 테이블 번호
            password: 비밀번호
        Returns:
            세션 토큰
        Raises:
            AuthenticationError: 인증 실패
            AccountLockedError: 계정 잠금
        """
        pass
    
    def verify_jwt_token(token: str) -> dict:
        """JWT 토큰 검증
        Args:
            token: JWT 토큰
        Returns:
            토큰 페이로드 (user_id, user_type, store_id)
        Raises:
            InvalidTokenError: 유효하지 않은 토큰
        """
        pass
    
    def verify_session_token(token: str) -> TableSession:
        """세션 토큰 검증
        Args:
            token: 세션 토큰
        Returns:
            TableSession 객체
        Raises:
            InvalidTokenError: 유효하지 않은 토큰
            SessionExpiredError: 세션 만료
        """
        pass
```

### MenuService
```python
class MenuService:
    """메뉴 서비스"""
    
    def get_menus_by_store(store_id: int) -> List[Menu]:
        """매장의 메뉴 목록 조회"""
        pass
    
    def create_menu(store_id: int, category_id: int, name: str, price: int, 
                   description: Optional[str], image_url: Optional[str]) -> Menu:
        """메뉴 생성
        Raises:
            ValidationError: 가격이 양수가 아님
        """
        pass
    
    def update_menu(menu_id: int, **kwargs) -> Menu:
        """메뉴 수정"""
        pass
    
    def delete_menu(menu_id: int) -> None:
        """메뉴 삭제"""
        pass
```

### OrderService
```python
class OrderService:
    """주문 서비스"""
    
    def create_order(session_token: str, items: List[dict]) -> Order:
        """주문 생성
        Args:
            session_token: 세션 토큰
            items: 주문 아이템 목록 [{"menu_id": 1, "quantity": 2}, ...]
        Returns:
            생성된 Order 객체
        Raises:
            SessionExpiredError: 세션 만료
            ValidationError: 수량이 양수가 아님
        """
        pass
    
    def get_orders_by_session(session_token: str) -> List[Order]:
        """세션의 주문 목록 조회"""
        pass
    
    def update_order_status(order_id: int, status: str) -> Order:
        """주문 상태 변경
        Raises:
            InvalidStatusTransitionError: 잘못된 상태 전이
        """
        pass
```

### SessionService
```python
class SessionService:
    """세션 서비스"""
    
    def check_session_expiry(session: TableSession) -> bool:
        """세션 만료 여부 확인
        Returns:
            True if expired, False otherwise
        """
        pass
    
    def close_session(session_id: int) -> None:
        """세션 종료 (매장 이용 완료)"""
        pass
```

---

## 4. API Layer (FastAPI Endpoints)

### Auth Endpoints
```python
@router.post("/api/auth/admin-login")
def admin_login(request: AdminLoginRequest) -> AdminLoginResponse:
    """관리자 로그인
    Request: {"store_id": 1, "username": "admin", "password": "password"}
    Response: {"token": "jwt-token", "expires_in": 57600}
    """
    pass

@router.post("/api/auth/table-login")
def table_login(request: TableLoginRequest) -> TableLoginResponse:
    """테이블 로그인
    Request: {"store_id": 1, "table_number": "T01", "password": "password"}
    Response: {"session_token": "uuid", "expires_in": 57600}
    """
    pass
```

### Menu Endpoints
```python
@router.get("/api/menus")
def get_menus(store_id: int) -> List[MenuResponse]:
    """메뉴 목록 조회"""
    pass

@router.post("/api/admin/menus")
def create_menu(request: CreateMenuRequest, token: str = Depends(verify_admin)) -> MenuResponse:
    """메뉴 생성 (관리자 전용)"""
    pass

@router.put("/api/admin/menus/{menu_id}")
def update_menu(menu_id: int, request: UpdateMenuRequest, token: str = Depends(verify_admin)) -> MenuResponse:
    """메뉴 수정 (관리자 전용)"""
    pass

@router.delete("/api/admin/menus/{menu_id}")
def delete_menu(menu_id: int, token: str = Depends(verify_admin)) -> None:
    """메뉴 삭제 (관리자 전용)"""
    pass
```

### Order Endpoints
```python
@router.post("/api/orders")
def create_order(request: CreateOrderRequest, session_token: str = Depends(verify_session)) -> OrderResponse:
    """주문 생성"""
    pass

@router.get("/api/orders")
def get_orders(session_token: str = Depends(verify_session)) -> List[OrderResponse]:
    """주문 목록 조회 (현재 세션)"""
    pass

@router.get("/api/admin/orders")
def get_all_orders(store_id: int, token: str = Depends(verify_admin)) -> List[OrderResponse]:
    """모든 주문 조회 (관리자 전용)"""
    pass

@router.put("/api/admin/orders/{order_id}/status")
def update_order_status(order_id: int, request: UpdateOrderStatusRequest, 
                       token: str = Depends(verify_admin)) -> OrderResponse:
    """주문 상태 변경 (관리자 전용)"""
    pass
```

### SSE Endpoint
```python
@router.get("/api/admin/sse/orders")
async def sse_orders(store_id: int, token: str = Depends(verify_admin)) -> EventSourceResponse:
    """실시간 주문 업데이트 (SSE)"""
    pass
```

### Health Check
```python
@router.get("/health")
def health_check() -> dict:
    """헬스 체크
    Response: {"status": "ok", "timestamp": "2026-02-09T12:00:00Z"}
    """
    pass
```

---

## 5. Utility Layer

### SecurityUtils
```python
class SecurityUtils:
    """보안 유틸리티"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """비밀번호 해싱 (bcrypt)"""
        pass
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증"""
        pass
    
    @staticmethod
    def create_jwt_token(payload: dict) -> str:
        """JWT 토큰 생성"""
        pass
    
    @staticmethod
    def verify_jwt_token(token: str) -> dict:
        """JWT 토큰 검증"""
        pass
```

### SessionUtils
```python
class SessionUtils:
    """세션 유틸리티"""
    
    @staticmethod
    def generate_session_token() -> str:
        """세션 토큰 생성 (UUID)"""
        pass
    
    @staticmethod
    def calculate_expiry_time(created_at: datetime, last_order_at: Optional[datetime]) -> datetime:
        """세션 만료 시간 계산
        Returns:
            16시간 OR 마지막 주문 후 2시간 중 먼저 도달하는 시간
        """
        pass
```

---

## Contract Summary

**Total Contracts**:
- Models: 8개 엔티티
- Repositories: 6개 클래스
- Services: 4개 클래스
- API Endpoints: 12개 엔드포인트
- Utilities: 2개 클래스

**Total Methods**: 약 50개 메서드

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
