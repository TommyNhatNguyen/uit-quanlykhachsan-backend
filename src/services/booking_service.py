from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.booking import Booking, CreateBooking, UpdateBooking
from src.repositories.booking_repo import BookingRepository


class BookingService:
    def __init__(self, repo: BookingRepository):
        self.repo = repo

    def get_booking(self, id: int) -> Booking:
        result = self.repo.get_booking(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Booking {id} not found")
        return result

    def get_list_bookings(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_bookings(page, page_size)

    def create_booking(self, booking: CreateBooking) -> Booking:
        return self.repo.create_booking(booking)

    def update_booking(self, id: int, data: UpdateBooking) -> Booking:
        current = self.repo.get_booking(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Booking {id} not found")
        merged = {**current.model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_booking(id, Booking(**merged))

    def delete_booking(self, id: int) -> Booking:
        current = self.repo.get_booking(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Booking {id} not found")
        self.repo.delete_booking(id)
        return current
