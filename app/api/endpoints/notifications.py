from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import session as db_session, models
from app.schemas import notification_schemas
from typing import List

router = APIRouter()

@router.get("/", response_model=List[notification_schemas.Notification])
def get_notifications(user_id: int, db: Session = Depends(db_session.get_db)):
    return db.query(models.Notification).filter_by(user_id=user_id).all()
