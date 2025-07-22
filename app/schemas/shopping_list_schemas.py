from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ShoppingListBase(BaseModel):
    user_id: int
    name: str
    created_at: datetime
    last_updated: datetime

class ShoppingListCreate(ShoppingListBase):
    pass

class ShoppingList(ShoppingListBase):
    list_id: int
    model_config = {"from_attributes": True}

class ShoppingListItemBase(BaseModel):
    list_id: int
    product_id: int
    quantity: int
    added_at: datetime

class ShoppingListItemCreate(ShoppingListItemBase):
    pass

class ShoppingListItem(ShoppingListItemBase):
    item_id: int
    model_config = {"from_attributes": True}
