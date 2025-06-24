from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from app.database import get_db
from app.models import User, Product, Order
from app.schemas import UserCreate, UserResponse, ProductCreate, ProductResponse, OrderCreate, OrderResponse
from app.crud import user_crud, product_crud, order_crud

app = FastAPI(
    title="内部向けAPI",
    description="内部システム用のAPI",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "内部向けAPI が稼働中です"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# ユーザー関連のエンドポイント
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[UserResponse])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_crud.get_users(db=db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    return user

# プロダクト関連のエンドポイント
@app.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return product_crud.create_product(db=db, product=product)

@app.get("/products/", response_model=List[ProductResponse])
async def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return product_crud.get_products(db=db, skip=skip, limit=limit)

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_crud.get_product(db=db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="プロダクトが見つかりません")
    return product

# 注文関連のエンドポイント
@app.post("/orders/", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_crud.create_order(db=db, order=order)

@app.get("/orders/", response_model=List[OrderResponse])
async def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return order_crud.get_orders(db=db, skip=skip, limit=limit)

@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    order = order_crud.get_order(db=db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="注文が見つかりません")
    return order

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001) 
