from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.booking import Booking, CreateBooking, UpdateBooking
from src.repositories.booking_repo import BookingRepository


class BookingService:
    def __init__(self, repo: BookingRepository):
        self.repo = repo

    def get_booking(self, booking_id: int) -> Booking:
        result = self.repo.get_booking(booking_id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found")
        return result

    def get_list_bookings(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_bookings(page, page_size)

    def create_booking(self, booking: CreateBooking) -> Booking:
        return self.repo.create_booking(booking)

    def update_booking(self, booking: UpdateBooking) -> Booking:
        current = self.repo.get_booking(booking.booking_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Booking {booking.booking_id} not found")
        merged_data = current.model_dump()
        merged_data.update(booking.model_dump(exclude_none=True))
        return self.repo.update_booking(UpdateBooking(**merged_data))

    def delete_booking(self, booking_id: int) -> Booking:
        current = self.repo.get_booking(booking_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found")
        self.repo.delete_booking(booking_id)
        return current
