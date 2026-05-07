from typing import Optional
from pydantic import BaseModel
from src.models.booking_detail import PopulatedBookingDetail
from src.models.service import Service

class ServicesDetail(BaseModel):
    id: int
    booking_detail_id: int
    service_id: int
    quanity: int
    price: float
    total_amount: float

class PopulatedServicesDetail(ServicesDetail):
    booking_detail: Optional[PopulatedBookingDetail] = None
    service: Optional[Service] = None

class CreateServicesDetail(BaseModel):
    booking_detail_id: int
    service_id: int
    quanity: int
    price: float
    total_amount: float

class UpdateServicesDetail(BaseModel):
    booking_detail_id: Optional[int] = None
    service_id: Optional[int] = None
    quanity: Optional[int] = None
    price: Optional[float] = None
    total_amount: Optional[float] = None