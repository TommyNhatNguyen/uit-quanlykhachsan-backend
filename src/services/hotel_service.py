from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.hotel import Hotel, CreateHotel, UpdateHotel
from src.repositories.hotel_repo import HotelRepository


class HotelService:
    def __init__(self, repo: HotelRepository):
        self.repo = repo

    def get_hotel(self, id: int) -> Hotel:
        result = self.repo.get_hotel(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Hotel {id} not found")
        return result

    def get_list_hotels(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_hotels(page, page_size)

    def create_hotel(self, hotel: CreateHotel) -> Hotel:
        return self.repo.create_hotel(hotel)

    def update_hotel(self, id: int, data: UpdateHotel) -> Hotel:
        current = self.repo.get_hotel(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Hotel {id} not found")
        merged = {**current.model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_hotel(id, Hotel(**merged))

    def delete_hotel(self, id: int) -> Hotel:
        current = self.repo.get_hotel(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Hotel {id} not found")
        self.repo.delete_hotel(id)
        return current
