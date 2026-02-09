"""Business logic services"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.models import AdminUser, TableAuth, TableSession, Menu, Order, OrderItem, OrderStatus
from src.utils import (
    hash_password, verify_password, create_jwt_token, 
    generate_session_token, is_session_expired
)

class AuthenticationError(Exception):
    pass

class AccountLockedError(Exception):
    pass

class InvalidTokenError(Exception):
    pass

class SessionExpiredError(Exception):
    pass

class ValidationError(Exception):
    pass

class InvalidStatusTransitionError(Exception):
    pass

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def login_admin(self, store_id: int, username: str, password: str) -> str:
        """Admin login with JWT token"""
        admin = self.db.query(AdminUser).filter(
            AdminUser.store_id == store_id,
            AdminUser.username == username
        ).first()
        
        if not admin:
            raise AuthenticationError("Invalid credentials")
        
        # Check if account is locked
        if admin.locked_until and admin.locked_until > datetime.utcnow():
            remaining = (admin.locked_until - datetime.utcnow()).seconds // 60
            raise AccountLockedError(f"Account locked. Try again in {remaining} minutes")
        
        # Verify password
        if not verify_password(password, admin.password_hash):
            admin.failed_login_attempts += 1
            if admin.failed_login_attempts >= 5:
                admin.locked_until = datetime.utcnow() + timedelta(minutes=15)
            self.db.commit()
            raise AuthenticationError("Invalid credentials")
        
        # Reset failed attempts on success
        admin.failed_login_attempts = 0
        admin.locked_until = None
        self.db.commit()
        
        # Create JWT token
        token_data = {
            "user_id": admin.id,
            "user_type": "admin",
            "store_id": admin.store_id
        }
        return create_jwt_token(token_data)
    
    def login_table(self, store_id: int, table_number: str, password: str) -> str:
        """Table login with session token"""
        table_auth = self.db.query(TableAuth).filter(
            TableAuth.store_id == store_id,
            TableAuth.table_number == table_number
        ).first()
        
        if not table_auth:
            raise AuthenticationError("Invalid credentials")
        
        # Check if account is locked
        if table_auth.locked_until and table_auth.locked_until > datetime.utcnow():
            remaining = (table_auth.locked_until - datetime.utcnow()).seconds // 60
            raise AccountLockedError(f"Account locked. Try again in {remaining} minutes")
        
        # Verify password
        if not verify_password(password, table_auth.password_hash):
            table_auth.failed_login_attempts += 1
            if table_auth.failed_login_attempts >= 5:
                table_auth.locked_until = datetime.utcnow() + timedelta(minutes=15)
            self.db.commit()
            raise AuthenticationError("Invalid credentials")
        
        # Reset failed attempts on success
        table_auth.failed_login_attempts = 0
        table_auth.locked_until = None
        self.db.commit()
        
        # Create new session
        session_token = generate_session_token()
        session = TableSession(
            table_auth_id=table_auth.id,
            session_token=session_token,
            is_active=True
        )
        self.db.add(session)
        self.db.commit()
        
        return session_token
    
    def verify_session_token(self, token: str) -> TableSession:
        """Verify session token and return session"""
        session = self.db.query(TableSession).filter(
            TableSession.session_token == token
        ).first()
        
        if not session:
            raise InvalidTokenError("Invalid session token")
        
        if not session.is_active:
            raise SessionExpiredError("Session is closed")
        
        if is_session_expired(session):
            session.is_active = False
            self.db.commit()
            raise SessionExpiredError("Session expired")
        
        return session

class MenuService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_menus_by_store(self, store_id: int):
        """Get available menus for a store"""
        from src.models import Category
        
        # Get menus
        menus = self.db.query(Menu).filter(
            Menu.store_id == store_id,
            Menu.is_available == True
        ).order_by(Menu.category_id, Menu.display_order).all()
        
        # Get categories
        categories = self.db.query(Category).filter(
            Category.store_id == store_id
        ).order_by(Category.display_order).all()
        
        return {
            "menus": menus,
            "categories": categories
        }
    
    def create_menu(self, store_id: int, category_id: int, name: str, 
                   price: int, description: str = None, image_url: str = None):
        """Create new menu"""
        if price <= 0:
            raise ValidationError("Price must be positive")
        
        menu = Menu(
            store_id=store_id,
            category_id=category_id,
            name=name,
            price=price,
            description=description,
            image_url=image_url
        )
        self.db.add(menu)
        self.db.commit()
        self.db.refresh(menu)
        return menu
    
    def update_menu(self, menu_id: int, **kwargs):
        """Update menu"""
        menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise ValidationError("Menu not found")
        
        if 'price' in kwargs and kwargs['price'] <= 0:
            raise ValidationError("Price must be positive")
        
        for key, value in kwargs.items():
            setattr(menu, key, value)
        
        self.db.commit()
        self.db.refresh(menu)
        return menu
    
    def delete_menu(self, menu_id: int):
        """Delete menu"""
        menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
        if menu:
            self.db.delete(menu)
            self.db.commit()

class OrderService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_order(self, session_token: str, items: list):
        """Create new order"""
        # Verify session
        auth_service = AuthService(self.db)
        session = auth_service.verify_session_token(session_token)
        
        # Validate items
        if not items:
            raise ValidationError("Order must have at least one item")
        
        # Create order
        order_number = f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{session.id:04d}"
        order = Order(
            store_id=session.table_auth.store_id,
            table_session_id=session.id,
            order_number=order_number,
            total_amount=0,
            status=OrderStatus.PENDING
        )
        self.db.add(order)
        self.db.flush()
        
        # Create order items
        total = 0
        for item_data in items:
            if item_data['quantity'] <= 0:
                raise ValidationError("Quantity must be positive")
            
            menu = self.db.query(Menu).filter(Menu.id == item_data['menu_id']).first()
            if not menu:
                raise ValidationError(f"Menu {item_data['menu_id']} not found")
            
            subtotal = menu.price * item_data['quantity']
            order_item = OrderItem(
                order_id=order.id,
                menu_id=menu.id,
                menu_name=menu.name,
                menu_price=menu.price,
                quantity=item_data['quantity'],
                subtotal=subtotal
            )
            self.db.add(order_item)
            total += subtotal
        
        order.total_amount = total
        
        # Update session last_order_at
        session.last_order_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def get_orders_by_session(self, session_token: str):
        """Get orders for a session"""
        auth_service = AuthService(self.db)
        session = auth_service.verify_session_token(session_token)
        
        return self.db.query(Order).filter(
            Order.table_session_id == session.id
        ).order_by(Order.created_at.desc()).all()
    
    def update_order_status(self, order_id: int, new_status: str):
        """Update order status with validation"""
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise ValidationError("Order not found")
        
        # Validate status transition
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.PREPARING],
            OrderStatus.PREPARING: [OrderStatus.COMPLETED],
            OrderStatus.COMPLETED: []
        }
        
        new_status_enum = OrderStatus(new_status)
        if new_status_enum not in valid_transitions.get(order.status, []):
            raise InvalidStatusTransitionError(
                f"Cannot transition from {order.status.value} to {new_status}"
            )
        
        order.status = new_status_enum
        self.db.commit()
        self.db.refresh(order)
        return order

class SessionService:
    def __init__(self, db: Session):
        self.db = db
    
    def close_session(self, session_id: int):
        """Close table session"""
        session = self.db.query(TableSession).filter(
            TableSession.id == session_id
        ).first()
        
        if session:
            session.is_active = False
            session.closed_at = datetime.utcnow()
            self.db.commit()
