"""Utility functions for security and session management"""
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
import uuid
from src.config import config

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

# JWT token management
def create_jwt_token(data: dict) -> str:
    """Create JWT token with expiration"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=config.JWT_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)

def verify_jwt_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

# Session management
def generate_session_token() -> str:
    """Generate unique session token"""
    return str(uuid.uuid4())

def calculate_expiry_time(created_at: datetime, last_order_at: datetime = None) -> datetime:
    """Calculate session expiry time
    Returns earlier of: created_at + 16h OR last_order_at + 2h
    """
    expiry_16h = created_at + timedelta(hours=config.SESSION_EXPIRE_HOURS)
    
    if last_order_at:
        expiry_2h = last_order_at + timedelta(hours=config.SESSION_LAST_ORDER_TIMEOUT_HOURS)
        return min(expiry_16h, expiry_2h)
    
    return expiry_16h

def is_session_expired(session) -> bool:
    """Check if session is expired"""
    now = datetime.utcnow()
    expiry = calculate_expiry_time(session.created_at, session.last_order_at)
    return now > expiry
