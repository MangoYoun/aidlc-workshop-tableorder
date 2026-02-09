"""Application configuration"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/tableorder")
    
    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", "16"))
    
    # Session
    SESSION_EXPIRE_HOURS = int(os.getenv("SESSION_EXPIRE_HOURS", "16"))
    SESSION_LAST_ORDER_TIMEOUT_HOURS = int(os.getenv("SESSION_LAST_ORDER_TIMEOUT_HOURS", "2"))
    
    # CORS
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
    
    # AWS
    AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-2")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "tableorder-menu-images")

config = Config()
