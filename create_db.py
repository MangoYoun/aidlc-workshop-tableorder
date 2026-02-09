"""Database schema creation script"""
from src.database import engine, Base
from src.models import (
    Store, AdminUser, TableAuth, TableSession,
    Category, Menu, Order, OrderItem
)

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    print("\nCreated tables:")
    print("- stores")
    print("- admin_users")
    print("- table_auths")
    print("- table_sessions")
    print("- categories")
    print("- menus")
    print("- orders")
    print("- order_items")

if __name__ == "__main__":
    create_tables()
