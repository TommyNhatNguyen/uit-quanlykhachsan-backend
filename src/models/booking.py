from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from src.models.customer import PopulatedCustomer
from src.models.booking_detail import (
    BookingStatus,
    PopulatedBookingDetail,
    CreateBookingDetail,
    UpdateBookingDetail,
)


class CreateBookingDetailInline(BaseModel):
    room_id: int
    checkin_date: datetime
    checkout_date: datetime
    quantity_of_nights: int
    price_per_night: float
    total_room_amount: float
    total_amount: float
    total_service_amount: Optional[float] = None
    status: BookingStatus = BookingStatus.BOOKED

# Re-export BookingStatus so existing code importing it from here still works
__all__ = ["BookingStatus", "Booking", "PopulatedBooking", "CreateBooking",
           "CreateBookingWithManyDetails", "UpdateBooking", "UpdateBookingWithManyDetails"]


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
    booking_details: List[CreateBookingDetailInline]
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


class QueryBookingsParams(BaseModel):
    page: int = 1
    page_size: int = 10
    customer_id: Optional[int] = None
