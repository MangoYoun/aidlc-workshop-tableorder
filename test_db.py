"""Test database connection"""
from src.database import SessionLocal
from src.models import Store

db = SessionLocal()
try:
    stores = db.query(Store).all()
    print(f"Found {len(stores)} stores:")
    for store in stores:
        print(f"  - ID: {store.id}, Name: {store.name}")
finally:
    db.close()
