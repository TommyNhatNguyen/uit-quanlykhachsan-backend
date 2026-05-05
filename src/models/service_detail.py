from typing import Optional
from pydantic import BaseModel


class ServiceDetail(BaseModel):
    service_detail: int
    booking_id: Optional[int] = None
    service_item_id: Optional[int] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    amount: Optional[float] = None

class CreateServiceDetail(BaseModel):
    service_detail: Optional[int] = None
    booking_id: Optional[int] = None
    service_item_id: Optional[int] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    amount: Optional[float] = None

class UpdateServiceDetail(BaseModel):
    service_detail: Optional[int] = None
    booking_id: Optional[int] = None
    service_item_id: Optional[int] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    amount: Optional[float] = None
