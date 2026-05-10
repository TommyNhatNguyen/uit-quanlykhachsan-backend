from fastapi import APIRouter
from src.db.db import db
from src.models.booking_detail import CreateBookingDetail, UpdateBookingDetail
from src.repositories.booking_detail_repo import BookingDetailRepository
from src.services.booking_detail_service import BookingDetailService

router = APIRouter(prefix="/api/booking-details", tags=["booking-details"])


def _svc() -> BookingDetailService:
    return BookingDetailService(BookingDetailRepository(db))


@router.get("")
def get_list_booking_details(page: int = 1, page_size: int = 10):
    return _svc().get_list_booking_details(page, page_size)


@router.get("/total-payments/{booking_id}")
def get_total_payments_by_booking_id(booking_id: int):
    return _svc().get_total_payments_by_booking_id(booking_id)


@router.get("/{id}")
def get_booking_detail(id: int):
    return _svc().get_booking_detail(id)


@router.post("")
def create_booking_detail(detail: CreateBookingDetail):
    return _svc().create_booking_detail(detail)


@router.put("/{id}")
def update_booking_detail(id: int, detail: UpdateBookingDetail):
    return _svc().update_booking_detail(id, detail)


@router.delete("/{id}")
def delete_booking_detail(id: int):
    return _svc().delete_booking_detail(id)
