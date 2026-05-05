from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.booking_detail import BookingDetail, CreateBookingDetail, UpdateBookingDetail
from src.repositories.booking_detail_repo import BookingDetailRepository


class BookingDetailService:
    def __init__(self, repo: BookingDetailRepository):
        self.repo = repo

    def get_booking_detail(self, booking_detail_id: int) -> BookingDetail:
        result = self.repo.get_booking_detail(booking_detail_id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"BookingDetail {booking_detail_id} not found")
        return result

    def get_list_booking_details(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_booking_details(page, page_size)

    def create_booking_detail(self, booking_detail: CreateBookingDetail) -> BookingDetail:
        return self.repo.create_booking_detail(booking_detail)

    def update_booking_detail(self, booking_detail: UpdateBookingDetail) -> BookingDetail:
        current = self.repo.get_booking_detail(booking_detail.booking_detail_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"BookingDetail {booking_detail.booking_detail_id} not found")
        merged_data = current.model_dump()
        merged_data.update(booking_detail.model_dump(exclude_none=True))
        return self.repo.update_booking_detail(UpdateBookingDetail(**merged_data))

    def delete_booking_detail(self, booking_detail_id: int) -> BookingDetail:
        current = self.repo.get_booking_detail(booking_detail_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"BookingDetail {booking_detail_id} not found")
        self.repo.delete_booking_detail(booking_detail_id)
        return current
