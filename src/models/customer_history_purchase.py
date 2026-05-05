from typing import Optional
from pydantic import BaseModel


class CustomerHistoryPurchase(BaseModel):
    id: int
    customer_id: Optional[int] = None
    booking_id: Optional[int] = None
    booking_paid: Optional[float] = None
    cumulative_paid: Optional[float] = None

class CreateCustomerHistoryPurchase(BaseModel):
    id: Optional[int] = None
    customer_id: Optional[int] = None
    booking_id: Optional[int] = None
    booking_paid: Optional[float] = None
    cumulative_paid: Optional[float] = None

class UpdateCustomerHistoryPurchase(BaseModel):
    id: Optional[int] = None
    customer_id: Optional[int] = None
    booking_id: Optional[int] = None
    booking_paid: Optional[float] = None
    cumulative_paid: Optional[float] = None
