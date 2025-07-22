from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import session as db_session, models
from app.schemas import favorite_schemas

router = APIRouter()

@router.post("/", response_model=favorite_schemas.Favorite)
def add_favorite(fav: favorite_schemas.FavoriteCreate, db: Session = Depends(db_session.get_db)):
    db_fav = models.Favorite(**fav.dict())
    db.add(db_fav)
    db.commit()
    db.refresh(db_fav)
    return db_fav

@router.get("/", response_model=List[favorite_schemas.Favorite])
def get_favorites(user_id: int, db: Session = Depends(db_session.get_db)):
    return db.query(models.Favorite).filter_by(user_id=user_id).all()

@router.delete("/{fav_id}", response_model=dict)
def remove_favorite(fav_id: int, db: Session = Depends(db_session.get_db)):
    fav = db.query(models.Favorite).filter(models.Favorite.id == fav_id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")
    db.delete(fav)
    db.commit()
    return {"detail": "Removed"}
