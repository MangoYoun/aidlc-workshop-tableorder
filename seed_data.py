"""Seed test data for TableOrder system"""
from src.database import SessionLocal
from src.models import Store, AdminUser, TableAuth, Category, Menu
import bcrypt

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def seed_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Store).first():
            print("⚠️  Data already exists. Skipping seed.")
            return
        
        # Create Store
        store = Store(
            name="맛있는 식당"
        )
        db.add(store)
        db.flush()
        
        # Create Admin User
        admin = AdminUser(
            store_id=store.id,
            username="admin",
            password_hash=hash_password("admin123")
        )
        db.add(admin)
        
        # Create Table Auths
        tables = [
            TableAuth(store_id=store.id, table_number="1", password_hash=hash_password("TABLE001")),
            TableAuth(store_id=store.id, table_number="2", password_hash=hash_password("TABLE002")),
            TableAuth(store_id=store.id, table_number="3", password_hash=hash_password("TABLE003")),
        ]
        db.add_all(tables)
        db.flush()
        
        # Create Categories
        categories = [
            Category(store_id=store.id, name="메인 요리", display_order=1),
            Category(store_id=store.id, name="사이드 메뉴", display_order=2),
            Category(store_id=store.id, name="음료", display_order=3),
        ]
        db.add_all(categories)
        db.flush()
        
        # Create Menus
        menus = [
            # Main dishes
            Menu(store_id=store.id, category_id=categories[0].id, name="불고기", 
                 description="한국식 불고기", price=15000, is_available=True, display_order=1),
            Menu(store_id=store.id, category_id=categories[0].id, name="비빔밥", 
                 description="야채 비빔밥", price=12000, is_available=True, display_order=2),
            Menu(store_id=store.id, category_id=categories[0].id, name="김치찌개", 
                 description="매운 김치찌개", price=10000, is_available=True, display_order=3),
            
            # Side dishes
            Menu(store_id=store.id, category_id=categories[1].id, name="김치", 
                 description="전통 김치", price=3000, is_available=True, display_order=1),
            Menu(store_id=store.id, category_id=categories[1].id, name="계란말이", 
                 description="부드러운 계란말이", price=5000, is_available=True, display_order=2),
            
            # Drinks
            Menu(store_id=store.id, category_id=categories[2].id, name="콜라", 
                 description="시원한 콜라", price=2000, is_available=True, display_order=1),
            Menu(store_id=store.id, category_id=categories[2].id, name="사이다", 
                 description="상쾌한 사이다", price=2000, is_available=True, display_order=2),
            Menu(store_id=store.id, category_id=categories[2].id, name="오렌지주스", 
                 description="신선한 오렌지주스", price=3000, is_available=True, display_order=3),
        ]
        db.add_all(menus)
        
        db.commit()
        
        print("✅ Test data created successfully!")
        print("\n📋 Test Credentials:")
        print("=" * 50)
        print(f"Store: {store.name}")
        print(f"Admin Username: admin")
        print(f"Admin Password: admin123")
        print(f"\nTable Passwords:")
        for i, table in enumerate(tables, 1):
            print(f"  - Table {table.table_number}: TABLE00{i}")
        print("=" * 50)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating test data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
