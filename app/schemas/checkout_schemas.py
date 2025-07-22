from pydantic import BaseModel

class CheckoutSummary(BaseModel):
    total_items: int
    total_price: float
    estimated_savings: float

    model_config = {"from_attributes": True}
