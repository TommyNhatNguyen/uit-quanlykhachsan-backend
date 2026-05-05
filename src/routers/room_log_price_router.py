from fastapi import APIRouter
from src.db.db import db
from src.models.room_log_price import CreateRoomLogPrice, UpdateRoomLogPrice
from src.repositories.room_log_price_repo import RoomLogPriceRepository
from src.services.room_log_price_service import RoomLogPriceService

router = APIRouter(prefix="/api/room-log-prices", tags=["room-log-prices"])


def _svc() -> RoomLogPriceService:
    return RoomLogPriceService(RoomLogPriceRepository(db))


@router.get("")
def get_list_room_log_prices(page: int = 1, page_size: int = 10):
    return _svc().get_list_room_log_prices(page, page_size)


@router.get("/{id}")
def get_room_log_price(id: int):
    return _svc().get_room_log_price(id)


@router.post("")
def create_room_log_price(log: CreateRoomLogPrice):
    return _svc().create_room_log_price(log)


@router.put("/{id}")
def update_room_log_price(id: int, log: UpdateRoomLogPrice):
    data = log.model_dump()
    data["id"] = id
    return _svc().update_room_log_price(UpdateRoomLogPrice(**data))


@router.delete("/{id}")
def delete_room_log_price(id: int):
    return _svc().delete_room_log_price(id)
