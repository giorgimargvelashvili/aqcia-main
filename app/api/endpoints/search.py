from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import session as db_session, models
from app.schemas import product_schemas
from typing import List

router = APIRouter()

@router.get("/", response_model=List[product_schemas.Product])
def search_products(q: str, db: Session = Depends(db_session.get_db)):
    return db.query(models.Product).filter(models.Product.name.ilike(f"%{q}%")).all()
