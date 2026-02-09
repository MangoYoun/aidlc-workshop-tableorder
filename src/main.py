"""FastAPI main application with all endpoints"""
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import time
import logging

from src.database import get_db, Base, engine
from src.services import (
    AuthService, MenuService, OrderService, SessionService,
    AuthenticationError, AccountLockedError, InvalidTokenError,
    SessionExpiredError, ValidationError, InvalidStatusTransitionError
)
from src.models import OrderStatus
from src.config import config
from src.utils import verify_jwt_token

# Create tables
Base.metadata.create_all(bind=engine)

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="TableOrder API", version="1.0.0")

# CORS middleware
origins = ["*"] if config.ENVIRONMENT == "development" else [config.FRONTEND_URL]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Timing middleware
@app.middleware("http")
async def timing_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    
    if process_time > 0.5:
        logger.warning(f"Slow API: {request.method} {request.url.path} took {process_time:.3f}s")
    
    return response

# Pydantic models
class AdminLoginRequest(BaseModel):
    store_id: int
    username: str
    password: str

class TableLoginRequest(BaseModel):
    store_id: int
    table_number: str
    password: str

class CreateMenuRequest(BaseModel):
    store_id: int
    category_id: int
    name: str
    price: int
    description: Optional[str] = None
    image_url: Optional[str] = None

class UpdateMenuRequest(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None

class OrderItemRequest(BaseModel):
    menu_id: int
    quantity: int

class CreateOrderRequest(BaseModel):
    items: List[OrderItemRequest]

class UpdateOrderStatusRequest(BaseModel):
    status: str

# Auth dependency
def verify_admin_token(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    token = authorization.replace("Bearer ", "")
    payload = verify_jwt_token(token)
    
    if not payload or payload.get("user_type") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return payload

def verify_session(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    token = authorization.replace("Bearer ", "")
    auth_service = AuthService(db)
    
    try:
        session = auth_service.verify_session_token(token)
        return session
    except (InvalidTokenError, SessionExpiredError) as e:
        raise HTTPException(status_code=401, detail=str(e))

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

# Auth endpoints
@app.post("/api/auth/admin-login")
def admin_login(request: AdminLoginRequest, db: Session = Depends(get_db)):
    try:
        auth_service = AuthService(db)
        token = auth_service.login_admin(request.store_id, request.username, request.password)
        return {"token": token, "expires_in": config.JWT_EXPIRE_HOURS * 3600}
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except AccountLockedError as e:
        raise HTTPException(status_code=403, detail=str(e))

@app.post("/api/auth/table-login")
def table_login(request: TableLoginRequest, db: Session = Depends(get_db)):
    try:
        auth_service = AuthService(db)
        token = auth_service.login_table(request.store_id, request.table_number, request.password)
        return {"session_token": token, "expires_in": config.SESSION_EXPIRE_HOURS * 3600}
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except AccountLockedError as e:
        raise HTTPException(status_code=403, detail=str(e))

# Menu endpoints
@app.get("/api/menus")
def get_menus(store_id: int, db: Session = Depends(get_db)):
    menu_service = MenuService(db)
    menus = menu_service.get_menus_by_store(store_id)
    return menus

@app.post("/api/admin/menus")
def create_menu(
    request: CreateMenuRequest,
    admin: dict = Depends(verify_admin_token),
    db: Session = Depends(get_db)
):
    try:
        menu_service = MenuService(db)
        menu = menu_service.create_menu(
            request.store_id, request.category_id, request.name,
            request.price, request.description, request.image_url
        )
        return menu
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/admin/menus/{menu_id}")
def update_menu(
    menu_id: int,
    request: UpdateMenuRequest,
    admin: dict = Depends(verify_admin_token),
    db: Session = Depends(get_db)
):
    try:
        menu_service = MenuService(db)
        menu = menu_service.update_menu(menu_id, **request.dict(exclude_unset=True))
        return menu
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/admin/menus/{menu_id}")
def delete_menu(
    menu_id: int,
    admin: dict = Depends(verify_admin_token),
    db: Session = Depends(get_db)
):
    menu_service = MenuService(db)
    menu_service.delete_menu(menu_id)
    return {"message": "Menu deleted"}

# Order endpoints
@app.post("/api/orders")
def create_order(
    request: CreateOrderRequest,
    session = Depends(verify_session),
    db: Session = Depends(get_db)
):
    try:
        order_service = OrderService(db)
        items = [item.dict() for item in request.items]
        order = order_service.create_order(session.session_token, items)
        return order
    except (ValidationError, SessionExpiredError) as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/orders")
def get_orders(
    session = Depends(verify_session),
    db: Session = Depends(get_db)
):
    order_service = OrderService(db)
    orders = order_service.get_orders_by_session(session.session_token)
    return orders

@app.get("/api/admin/orders")
def get_all_orders(
    store_id: int,
    admin: dict = Depends(verify_admin_token),
    db: Session = Depends(get_db)
):
    from src.models import Order
    orders = db.query(Order).filter(Order.store_id == store_id).order_by(Order.created_at.desc()).all()
    return orders

@app.put("/api/admin/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    request: UpdateOrderStatusRequest,
    admin: dict = Depends(verify_admin_token),
    db: Session = Depends(get_db)
):
    try:
        order_service = OrderService(db)
        order = order_service.update_order_status(order_id, request.status)
        return order
    except (ValidationError, InvalidStatusTransitionError) as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/admin/sessions/{session_id}/close")
def close_session(
    session_id: int,
    admin: dict = Depends(verify_admin_token),
    db: Session = Depends(get_db)
):
    session_service = SessionService(db)
    session_service.close_session(session_id)
    return {"message": "Session closed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
