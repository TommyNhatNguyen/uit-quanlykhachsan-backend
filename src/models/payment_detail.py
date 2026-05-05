from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class PaymentDetail(BaseModel):
    payment_detail_id: int
    cashier_id: Optional[int] = None
    payment_id: Optional[int] = None
    total_payment: Optional[float] = None
    payment_method: Optional[str] = None
    payment_datetime: Optional[datetime] = None

class CreatePaymentDetail(BaseModel):
    payment_detail_id: Optional[int] = None
    cashier_id: Optional[int] = None
    payment_id: Optional[int] = None
    total_payment: Optional[float] = None
    payment_method: Optional[str] = None
    payment_datetime: Optional[datetime] = None

class UpdatePaymentDetail(BaseModel):
    payment_detail_id: Optional[int] = None
    cashier_id: Optional[int] = None
    payment_id: Optional[int] = None
    total_payment: Optional[float] = None
    payment_method: Optional[str] = None
    payment_datetime: Optional[datetime] = None
