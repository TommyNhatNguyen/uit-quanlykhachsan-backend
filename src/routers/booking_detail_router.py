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


@router.get("/{booking_detail_id}")
def get_booking_detail(booking_detail_id: int):
    return _svc().get_booking_detail(booking_detail_id)


@router.post("")
def create_booking_detail(booking_detail: CreateBookingDetail):
    return _svc().create_booking_detail(booking_detail)


@router.put("/{booking_detail_id}")
def update_booking_detail(booking_detail_id: int, booking_detail: UpdateBookingDetail):
    data = booking_detail.model_dump()
    data["booking_detail_id"] = booking_detail_id
    return _svc().update_booking_detail(UpdateBookingDetail(**data))


@router.delete("/{booking_detail_id}")
def delete_booking_detail(booking_detail_id: int):
    return _svc().delete_booking_detail(booking_detail_id)
