from pydantic import BaseModel
from typing import Optional

class ProductResponse(BaseModel):
    product_id: int
    name: str
    brand: str
    price: float
    sale_price: Optional[float]
    is_on_sale: bool
    available_quantity: int

    model_config = {"from_attributes": True}

class CategoryBase(BaseModel):
    name: str
    name_ka: str
    name_en: str
    name_ru: str
    icon: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True
