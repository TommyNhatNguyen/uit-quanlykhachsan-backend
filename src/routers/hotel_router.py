from fastapi import APIRouter
from src.db.db import db
from src.models.hotel import CreateHotel, UpdateHotel
from src.repositories.hotel_repo import HotelRepository
from src.services.hotel_service import HotelService

router = APIRouter(prefix="/api/hotels", tags=["hotels"])


def _svc() -> HotelService:
    return HotelService(HotelRepository(db))


@router.get("")
def get_list_hotels(page: int = 1, page_size: int = 10):
    return _svc().get_list_hotels(page, page_size)


@router.get("/{id}")
def get_hotel(id: int):
    return _svc().get_hotel(id)


@router.post("")
def create_hotel(hotel: CreateHotel):
    return _svc().create_hotel(hotel)


@router.put("/{id}")
def update_hotel(id: int, hotel: UpdateHotel):
    return _svc().update_hotel(id, hotel)


@router.delete("/{id}")
def delete_hotel(id: int):
    return _svc().delete_hotel(id)
