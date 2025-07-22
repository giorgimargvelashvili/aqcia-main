from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import session as db_session, models
from app.schemas import sale_alert_schemas
from typing import List

router = APIRouter()

@router.post("/", response_model=sale_alert_schemas.SaleAlert)
def create_sale_alert(alert: sale_alert_schemas.SaleAlertCreate, db: Session = Depends(db_session.get_db)):
    db_alert = models.SaleAlert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.get("/", response_model=List[sale_alert_schemas.SaleAlert])
def get_sale_alerts(user_id: int, db: Session = Depends(db_session.get_db)):
    return db.query(models.SaleAlert).filter_by(user_id=user_id).all()
