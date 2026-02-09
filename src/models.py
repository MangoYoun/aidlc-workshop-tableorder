"""Database models - All entities in one file"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from src.database import Base
import enum

class OrderStatus(enum.Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    COMPLETED = "completed"

class Store(Base):
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    admin_users = relationship("AdminUser", back_populates="store")
    table_auths = relationship("TableAuth", back_populates="store")
    categories = relationship("Category", back_populates="store")
    menus = relationship("Menu", back_populates="store")
    orders = relationship("Order", back_populates="store")

class AdminUser(Base):
    __tablename__ = "admin_users"
    __table_args__ = (
        {'sqlite_autoincrement': True},
    )
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    username = Column(String(50), nullable=False)
    password_hash = Column(String(255), nullable=False)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    store = relationship("Store", back_populates="admin_users")

class TableAuth(Base):
    __tablename__ = "table_auths"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    table_number = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    store = relationship("Store", back_populates="table_auths")
    sessions = relationship("TableSession", back_populates="table_auth")

class TableSession(Base):
    __tablename__ = "table_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    table_auth_id = Column(Integer, ForeignKey("table_auths.id"), nullable=False)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_order_at = Column(DateTime, nullable=True)
    expired_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    table_auth = relationship("TableAuth", back_populates="sessions")
    orders = relationship("Order", back_populates="table_session")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    name = Column(String(50), nullable=False)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    store = relationship("Store", back_populates="categories")
    menus = relationship("Menu", back_populates="category")

class Menu(Base):
    __tablename__ = "menus"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)
    image_url = Column(String(500), nullable=True)
    display_order = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    store = relationship("Store", back_populates="menus")
    category = relationship("Category", back_populates="menus")
    order_items = relationship("OrderItem", back_populates="menu")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    table_session_id = Column(Integer, ForeignKey("table_sessions.id"), nullable=False)
    order_number = Column(String(20), unique=True, nullable=False, index=True)
    total_amount = Column(Integer, nullable=False)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    store = relationship("Store", back_populates="orders")
    table_session = relationship("TableSession", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)
    menu_name = Column(String(100), nullable=False)
    menu_price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    order = relationship("Order", back_populates="order_items")
    menu = relationship("Menu", back_populates="order_items")
