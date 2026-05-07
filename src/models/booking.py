from typing import Optional, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

from src.models.customer import PopulatedCustomer
from src.models.booking_detail import CreateBookingDetail, PopulatedBookingDetail, UpdateBookingDetail

class BookingStatus(str, Enum):
    BOOKED = "BOOKED"
    CANCELED = "CANCELED"
    CHECKIN = "CHECKIN"
    CHECKOUT = "CHECKOUT"


class Booking(BaseModel):
    id: int
    customer_id: int
    created_at: Optional[datetime]
    notes: Optional[str]
    is_fully_paid: bool
    is_deleted: bool


class PopulatedBooking(Booking):
    customer: Optional[PopulatedCustomer] = None
    booking_details: Optional[List[PopulatedBookingDetail]] = None


class CreateBooking(BaseModel):
    customer_id: int
    notes: Optional[str] = None
    is_fully_paid: Optional[bool] = False
    created_at: datetime = datetime.now()

class CreateBookingWithManyDetails(BaseModel):
    customer_id: int
    notes: Optional[str] = None
    is_fully_paid: Optional[bool] = False
    booking_details: List[CreateBookingDetail]
    created_at: datetime = datetime.now()

class UpdateBooking(BaseModel):
    customer_id: Optional[int] = None
    created_at: Optional[datetime] = None
    notes: Optional[str] = None
    is_fully_paid: Optional[bool] = None
    is_deleted: Optional[bool] = None

class UpdateBookingWithManyDetails(BaseModel):
    customer_id: Optional[int] = None
    created_at: Optional[datetime] = None
    notes: Optional[str] = None
    is_fully_paid: Optional[bool] = None
    is_deleted: Optional[bool] = None
    booking_details: Optional[List[UpdateBookingDetail]] = None