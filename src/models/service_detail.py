from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel

from src.models.service import Service

if TYPE_CHECKING:
    from src.models.booking_detail import BookingDetail


class ServicesDetail(BaseModel):
    id: int
    booking_detail_id: int
    service_id: int
    quanity: int
    price: float
    total_amount: float


class PopulatedServicesDetail(ServicesDetail):
    booking_detail: Optional["BookingDetail"] = None
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
