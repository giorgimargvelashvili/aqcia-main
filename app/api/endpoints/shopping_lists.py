from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import session as db_session, models
from app.schemas import shopping_list_schemas
from typing import List

router = APIRouter()

@router.post("/", response_model=shopping_list_schemas.ShoppingList)
def create_shopping_list(list_in: shopping_list_schemas.ShoppingListCreate, db: Session = Depends(db_session.get_db)):
    db_list = models.ShoppingList(**list_in.dict())
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

@router.get("/", response_model=List[shopping_list_schemas.ShoppingList])
def get_shopping_lists(user_id: int, db: Session = Depends(db_session.get_db)):
    return db.query(models.ShoppingList).filter_by(user_id=user_id).all()
