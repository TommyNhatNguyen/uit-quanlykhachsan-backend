from typing import Optional
from pydantic import BaseModel


class Payment(BaseModel):
    payment_id: int
    status: Optional[str] = None

class CreatePayment(BaseModel):
    payment_id: Optional[int] = None
    status: Optional[str] = None

class UpdatePayment(BaseModel):
    payment_id: Optional[int] = None
    status: Optional[str] = None
