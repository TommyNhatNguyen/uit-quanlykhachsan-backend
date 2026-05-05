from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Booking(BaseModel):
    booking_id: int
    customer_id: int
    checkin_datetime: Optional[datetime] = None
    checkout_datetime: Optional[datetime] = None
    status: Optional[str] = None
    payment_id: Optional[int] = None    
    hotel_id: Optional[int] = None
    created_at: Optional[datetime] = None
    notes: Optional[str] = None

class CreateBooking(BaseModel):
    booking_id: Optional[int] = None
    customer_id: Optional[int] = None
    checkin_datetime: Optional[datetime] = None
    checkout_datetime: Optional[datetime] = None
    status: Optional[str] = None
    payment_id: Optional[int] = None
    hotel_id: Optional[int] = None
    created_at: Optional[datetime] = None
    notes: Optional[str] = None

class UpdateBooking(BaseModel):
    booking_id: Optional[int] = None
    customer_id: Optional[int] = None
    checkin_datetime: Optional[datetime] = None
    checkout_datetime: Optional[datetime] = None
    status: Optional[str] = None
    payment_id: Optional[int] = None
    hotel_id: Optional[int] = None
    created_at: Optional[datetime] = None
    notes: Optional[str] = None

