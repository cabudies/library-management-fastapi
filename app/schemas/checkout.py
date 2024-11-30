from pydantic import BaseModel
from datetime import datetime

class CheckoutCreate(BaseModel):
    item_copy_id: int

class CheckoutReturn(BaseModel):
    checkout_id: int

class Checkout(BaseModel):
    id: int
    user_id: int
    item_copy_id: int
    checkout_date: datetime
    return_date: datetime | None

    class Config:
        from_attributes = True 