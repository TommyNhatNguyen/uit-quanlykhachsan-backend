from typing import Annotated
from fastapi import APIRouter, Depends
from src.db.db import db
from src.models.booking import CreateBooking, CreateBookingWithManyDetails, UpdateBooking, UpdateBookingWithManyDetails, QueryBookingsParams
from src.repositories.booking_repo import BookingRepository
from src.repositories.booking_detail_repo import BookingDetailRepository
from src.services.booking_service import BookingService

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


def _svc() -> BookingService:
    return BookingService(BookingRepository(db), BookingDetailRepository(db))


@router.get("")
def get_list_bookings(params: Annotated[QueryBookingsParams, Depends()]):
    return _svc().get_list_bookings(params)


@router.get("/{id}")
def get_booking(id: int):
    return _svc().get_booking(id)


@router.post("")
def create_booking(booking: CreateBooking):
    return _svc().create_booking(booking)


@router.post("/with-details")
def create_booking_with_details(data: CreateBookingWithManyDetails):
    return _svc().create_booking_with_details(data)


@router.put("/{id}")
def update_booking(id: int, booking: UpdateBooking):
    return _svc().update_booking(id, booking)


@router.put("/with-details/{id}")
def update_booking_with_details(id: int, data: UpdateBookingWithManyDetails):
    return _svc().update_booking_with_details(id, data)


@router.delete("/{id}")
def delete_booking(id: int):
    return _svc().delete_booking(id)
