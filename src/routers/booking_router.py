from fastapi import APIRouter
from src.db.db import db
from src.models.booking import CreateBooking, UpdateBooking
from src.repositories.booking_repo import BookingRepository
from src.services.booking_service import BookingService

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


def _svc() -> BookingService:
    return BookingService(BookingRepository(db))


@router.get("")
def get_list_bookings(page: int = 1, page_size: int = 10):
    return _svc().get_list_bookings(page, page_size)


@router.get("/{id}")
def get_booking(id: int):
    return _svc().get_booking(id)


@router.post("")
def create_booking(booking: CreateBooking):
    return _svc().create_booking(booking)


@router.put("/{id}")
def update_booking(id: int, booking: UpdateBooking):
    return _svc().update_booking(id, booking)


@router.delete("/{id}")
def delete_booking(id: int):
    return _svc().delete_booking(id)
