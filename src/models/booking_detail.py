from typing import Optional
from pydantic import BaseModel


class BookingDetail(BaseModel):
    booking_detail_id: int
    booking_id: Optional[int] = None
    room_id: Optional[int] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    amount: Optional[float] = None

class CreateBookingDetail(BaseModel):
    booking_detail_id: Optional[int] = None
    booking_id: Optional[int] = None
    room_id: Optional[int] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    amount: Optional[float] = None

class UpdateBookingDetail(BaseModel):
    booking_detail_id: Optional[int] = None
    booking_id: Optional[int] = None
    room_id: Optional[int] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    amount: Optional[float] = None
