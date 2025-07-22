from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import session as db_session, models
from app.schemas import product_schemas
from typing import List

router = APIRouter()

@router.post("/", response_model=product_schemas.Inventory)
def create_or_update_inventory(inv: product_schemas.InventoryCreate, db: Session = Depends(db_session.get_db)):
    db_inv = db.query(models.Inventory).filter_by(store_id=inv.store_id, product_id=inv.product_id).first()
    if db_inv:
        for field, value in inv.dict().items():
            setattr(db_inv, field, value)
    else:
        db_inv = models.Inventory(**inv.dict())
        db.add(db_inv)
    db.commit()
    db.refresh(db_inv)
    return db_inv

@router.get("/product/{product_id}", response_model=List[product_schemas.Inventory])
def get_inventory_for_product(product_id: int, db: Session = Depends(db_session.get_db)):
    return db.query(models.Inventory).filter_by(product_id=product_id).all() 