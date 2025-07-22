from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationBase(BaseModel):
    user_id: int
    product_id: int
    store_id: Optional[int] = None
    type: str
    message: str
    sent_at: datetime
    is_read: Optional[bool] = False
    extra_metadata: Optional[dict] = None

class Notification(NotificationBase):
    notification_id: int
    model_config = {"from_attributes": True}
