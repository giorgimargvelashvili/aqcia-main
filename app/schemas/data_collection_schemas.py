from pydantic import BaseModel
from typing import Optional

class ProductData(BaseModel):
    name: str
    brand: Optional[str]
    type: Optional[str]
    size: Optional[str]
    upc: Optional[str]
    keywords: Optional[str]
    price: float
    sale_price: Optional[float]
    is_on_sale: Optional[bool] = False
    sale_start: Optional[str]
    sale_end: Optional[str]
    store_name: str
    store_location: str
    api_source: Optional[str]
    quantity: Optional[int]
    last_restocked: Optional[str] 