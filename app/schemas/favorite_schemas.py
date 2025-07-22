from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FavoriteBase(BaseModel):
    user_id: int
    product_id: int
    added_at: datetime
    notify_on_sale: Optional[bool] = False

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    favorite_id: int
    model_config = {"from_attributes": True}
