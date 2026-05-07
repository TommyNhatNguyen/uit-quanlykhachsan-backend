from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from src.models.booking import BookingStatus
from src.models.booking import PopulatedBooking
from src.models.room import PopulatedRoom
from src.models.payment import PopulatedPayment
from src.models.service_detail import PopulatedServicesDetail

class BookingDetail(BaseModel):
    id: int
    booking_id: int
    room_id: int
    checkin_date: datetime
    checkout_date: datetime
    quantity_of_nights: int
    price_per_night: float
    total_room_amount: float
    total_service_amount: Optional[float]
    total_amount: float
    is_fully_paid: bool
    status: BookingStatus


class PopulatedBookingDetail(BookingDetail):
    booking: Optional[PopulatedBooking] = None
    room: Optional[PopulatedRoom] = None
    payments: Optional[List[PopulatedPayment]] = None
    services_details: Optional[List[PopulatedServicesDetail]] = None

class CreateBookingDetail(BaseModel):
    booking_id: int
    room_id: int
    checkin_date: datetime
    checkout_date: datetime
    quantity_of_nights: int
    price_per_night: float
    total_room_amount: float
    total_amount: float
    total_service_amount: Optional[float] = None
    status: BookingStatus = BookingStatus.BOOKED


class UpdateBookingDetail(BaseModel):
    booking_id: Optional[int] = None
    room_id: Optional[int] = None
    checkin_date: Optional[datetime] = None
    checkout_date: Optional[datetime] = None
    quantity_of_nights: Optional[int] = None
    price_per_night: Optional[float] = None
    total_room_amount: Optional[float] = None
    total_service_amount: Optional[float] = None
    total_amount: Optional[float] = None
    is_fully_paid: Optional[bool] = None
    status: Optional[BookingStatus] = None