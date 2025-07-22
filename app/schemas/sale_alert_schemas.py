from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SaleAlertBase(BaseModel):
    user_id: int
    product_id: int
    notify_on_sale: Optional[bool] = True
    notify_if_already_on_sale: Optional[bool] = False
    is_active: Optional[bool] = True
    created_at: datetime
    last_notified: Optional[datetime] = None

class SaleAlertCreate(SaleAlertBase):
    pass

class SaleAlert(SaleAlertBase):
    alert_id: int
    model_config = {"from_attributes": True}
