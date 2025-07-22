from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: str
    location: str
    location_permission_granted: bool
    notification_preferences: str
    created_at: datetime

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: int
    model_config = {"from_attributes": True}
