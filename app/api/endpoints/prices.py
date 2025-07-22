from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import session as db_session, models
from app.schemas import product_schemas
from typing import List

router = APIRouter()

@router.post("/", response_model=product_schemas.Price)
def create_or_update_price(price: product_schemas.PriceCreate, db: Session = Depends(db_session.get_db)):
    # Upsert logic for price
    db_price = db.query(models.Price).filter_by(store_id=price.store_id, product_id=price.product_id).first()
    if db_price:
        for field, value in price.dict().items():
            setattr(db_price, field, value)
    else:
        db_price = models.Price(**price.dict())
        db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price

@router.get("/product/{product_id}", response_model=List[product_schemas.Price])
def get_prices_for_product(product_id: int, db: Session = Depends(db_session.get_db)):
    return db.query(models.Price).filter_by(product_id=product_id).all() 