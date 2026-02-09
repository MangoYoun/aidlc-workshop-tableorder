"""Test cases for services - Skeleton for TDD"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.models import Store, AdminUser, TableAuth, TableSession, Menu, Category
from src.services import AuthService, MenuService, OrderService, SessionService
from src.services import AuthenticationError, AccountLockedError, ValidationError
from src.utils import hash_password

# Test database setup
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_store(db):
    store = Store(name="Test Store")
    db.add(store)
    db.commit()
    db.refresh(store)
    return store

@pytest.fixture
def sample_admin(db, sample_store):
    admin = AdminUser(
        store_id=sample_store.id,
        username="admin",
        password_hash=hash_password("password123")
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

# TC-BS-001: Valid admin login
def test_admin_login_success(db, sample_admin):
    auth_service = AuthService(db)
    token = auth_service.login_admin(sample_admin.store_id, "admin", "password123")
    assert token is not None
    assert len(token) > 0

# TC-BS-002: Invalid password
def test_admin_login_invalid_password(db, sample_admin):
    auth_service = AuthService(db)
    with pytest.raises(AuthenticationError):
        auth_service.login_admin(sample_admin.store_id, "admin", "wrongpassword")

# TC-BS-003: Account lock after 5 failures
def test_admin_login_account_lock(db, sample_admin):
    auth_service = AuthService(db)
    
    # Fail 5 times
    for i in range(5):
        try:
            auth_service.login_admin(sample_admin.store_id, "admin", "wrongpassword")
        except AuthenticationError:
            pass
    
    # 6th attempt should raise AccountLockedError
    with pytest.raises(AccountLockedError):
        auth_service.login_admin(sample_admin.store_id, "admin", "wrongpassword")

# TC-BS-012: Create menu with valid data
def test_create_menu_success(db, sample_store):
    category = Category(store_id=sample_store.id, name="Main")
    db.add(category)
    db.commit()
    
    menu_service = MenuService(db)
    menu = menu_service.create_menu(
        store_id=sample_store.id,
        category_id=category.id,
        name="Test Menu",
        price=10000
    )
    assert menu.id is not None
    assert menu.name == "Test Menu"
    assert menu.price == 10000

# TC-BS-013: Create menu with invalid price
def test_create_menu_invalid_price(db, sample_store):
    category = Category(store_id=sample_store.id, name="Main")
    db.add(category)
    db.commit()
    
    menu_service = MenuService(db)
    with pytest.raises(ValidationError):
        menu_service.create_menu(
            store_id=sample_store.id,
            category_id=category.id,
            name="Test Menu",
            price=-1000
        )

# Add more test cases following the test plan...
# TC-BS-014 to TC-BS-036 would be implemented here
