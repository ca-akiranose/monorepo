from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from app.database import get_db
from app.models import Product, Order
from app.schemas import ProductResponse, OrderCreate, OrderResponse
from app.crud import product_crud, order_crud

# レート制限の設定
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="外部向けAPI",
    description="外部クライアント用のAPI",
    version="1.0.0"
)

# レート制限の追加
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
@limiter.limit("5/minute")
async def root(request):
    return {"message": "外部向けAPI が稼働中です"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# プロダクト関連のエンドポイント（読み取り専用）
@app.get("/products/", response_model=List[ProductResponse])
@limiter.limit("100/minute")
async def get_products(request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return product_crud.get_products(db=db, skip=skip, limit=limit)

@app.get("/products/{product_id}", response_model=ProductResponse)
@limiter.limit("100/minute")
async def get_product(request, product_id: int, db: Session = Depends(get_db)):
    product = product_crud.get_product(db=db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="プロダクトが見つかりません")
    return product

# 注文関連のエンドポイント
@app.post("/orders/", response_model=OrderResponse)
@limiter.limit("10/minute")
async def create_order(request, order: OrderCreate, db: Session = Depends(get_db)):
    return order_crud.create_order(db=db, order=order)

@app.get("/orders/{order_id}", response_model=OrderResponse)
@limiter.limit("50/minute")
async def get_order(request, order_id: int, db: Session = Depends(get_db)):
    order = order_crud.get_order(db=db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="注文が見つかりません")
    return order

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3002) 
