from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.booking_detail import BookingDetail, CreateBookingDetail, UpdateBookingDetail
from src.repositories.booking_detail_repo import BookingDetailRepository


class BookingDetailService:
    def __init__(self, repo: BookingDetailRepository):
        self.repo = repo

    def get_booking_detail(self, id: int) -> BookingDetail:
        result = self.repo.get_booking_detail(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"BookingDetail {id} not found")
        return result

    def get_list_booking_details(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_booking_details(page, page_size)

    def create_booking_detail(self, detail: CreateBookingDetail) -> BookingDetail:
        return self.repo.create_booking_detail(detail)

    def update_booking_detail(self, id: int, data: UpdateBookingDetail) -> BookingDetail:
        current = self.repo.get_booking_detail(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"BookingDetail {id} not found")
        merged = {**current.model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_booking_detail(id, BookingDetail(**merged))

    def get_total_payments_by_booking_id(self, booking_id: int):
        return self.repo.get_total_payments_by_booking_id(booking_id)

    def delete_booking_detail(self, id: int) -> BookingDetail:
        current = self.repo.get_booking_detail(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"BookingDetail {id} not found")
        self.repo.delete_booking_detail(id)
        return current
