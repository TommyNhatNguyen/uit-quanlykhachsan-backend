from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.booking import Booking, CreateBooking, CreateBookingWithManyDetails, UpdateBooking, UpdateBookingWithManyDetails, QueryBookingsParams
from src.models.booking_detail import BookingDetail, CreateBookingDetail
from src.repositories.booking_repo import BookingRepository
from src.repositories.booking_detail_repo import BookingDetailRepository


class BookingService:
    def __init__(self, repo: BookingRepository, detail_repo: BookingDetailRepository):
        self.repo = repo
        self.detail_repo = detail_repo

    def get_booking(self, id: int) -> Booking:
        result = self.repo.get_booking(id)
        if not result or isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Booking {id} not found")
        return result

    def get_list_bookings(self, params: QueryBookingsParams) -> dict:
        return self.repo.get_list_bookings(params)

    def create_booking(self, booking: CreateBooking) -> Booking:
        return self.repo.create_booking(booking)

    def create_booking_with_details(self, data: CreateBookingWithManyDetails) -> Booking:
        booking = self.repo.create_booking(CreateBooking(
            customer_id=data.customer_id,
            notes=data.notes,
            is_fully_paid=data.is_fully_paid,
            created_at=data.created_at,
        ))
        if isinstance(booking, JSONResponse):
            raise HTTPException(status_code=500, detail="Failed to create booking")
        for detail in data.booking_details:
            result = self.detail_repo.create_booking_detail(CreateBookingDetail(
                customer_id=booking.customer_id,
                booking_id=booking.id,
                room_id=detail.room_id,
                checkin_date=detail.checkin_date,
                checkout_date=detail.checkout_date,
                quantity_of_nights=detail.quantity_of_nights,
                price_per_night=detail.price_per_night,
                total_room_amount=detail.total_room_amount,
                total_service_amount=detail.total_service_amount,
                total_amount=detail.total_amount,
                status=detail.status,
            ))
            if isinstance(result, JSONResponse):
                raise HTTPException(status_code=500, detail=f"Failed to create detail for room {detail.room_id}")
        return self.repo.get_booking(booking.id)

    def update_booking_with_details(self, id: int, data: UpdateBookingWithManyDetails) -> Booking:
        current = self.repo.get_booking(id)
        if not current or isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Booking {id} not found")
        booking_fields = data.model_dump(exclude={'booking_details'}, exclude_none=True)
        if booking_fields:
            merged = {**Booking(**current.model_dump()).model_dump(), **booking_fields}
            self.repo.update_booking(id, Booking(**merged))
        if data.booking_details:
            for detail in data.booking_details:
                if not detail.id:
                    raise HTTPException(status_code=400, detail="Each booking detail must include an 'id' to update")
                current_detail = self.detail_repo.get_booking_detail(detail.id)
                if not current_detail or isinstance(current_detail, JSONResponse):
                    raise HTTPException(status_code=404, detail=f"BookingDetail {detail.id} not found")
                merged_detail = {**current_detail.model_dump(), **detail.model_dump(exclude_none=True, exclude={'id'})}
                self.detail_repo.update_booking_detail(detail.id, BookingDetail(**merged_detail))
        return self.repo.get_booking(id)

    def update_booking(self, id: int, data: UpdateBooking) -> Booking:
        current = self.repo.get_booking(id)
        if not current or isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Booking {id} not found")
        merged = {**Booking(**current.model_dump()).model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_booking(id, Booking(**merged))

    def delete_booking(self, id: int) -> Booking:
        current = self.repo.get_booking(id)
        if not current or isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Booking {id} not found")
        self.repo.delete_booking(id)
        return current
