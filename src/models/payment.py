from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from src.models.booking_detail import PopulatedBookingDetail
from src.models.employee import PopulatedEmployee


class Payment(BaseModel):
    id: int
    cashier_id: int
    total_payment: float
    payment_method: str
    booking_detail_id: int
    created_at: Optional[datetime]
    is_deleted: bool


class PopulatedPayment(Payment):
    cashier: Optional[PopulatedEmployee] = None
    booking_detail: Optional[PopulatedBookingDetail] = None


class CreatePayment(BaseModel):
    cashier_id: int
    total_payment: float
    payment_method: str
    booking_detail_id: int
    created_at: datetime = datetime.now()


class UpdatePayment(BaseModel):
    cashier_id: Optional[int] = None
    total_payment: Optional[float] = None
    payment_method: Optional[str] = None
    booking_detail_id: Optional[int] = None
    created_at: Optional[datetime] = None
    is_deleted: Optional[bool] = None