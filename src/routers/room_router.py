from typing import Annotated
from fastapi import APIRouter, Depends
from src.db.db import db
from src.models.room import AvailableRoomsParams, CreateRoom, QueryRoomsParams, UpdateRoom, UpdateRoomPrice
from src.repositories.room_log_price_repo import RoomPriceLogRepository
from src.repositories.room_repo import RoomRepository
from src.services.room_log_price_service import RoomPriceLogService
from src.services.room_service import RoomService

router = APIRouter(prefix="/api/rooms", tags=["rooms"])


def _svc() -> RoomService:
    return RoomService(RoomRepository(db), roomPriceLogSerivce=RoomPriceLogService(RoomPriceLogRepository(db)))


@router.get("")
def get_list_rooms(params: Annotated[QueryRoomsParams, Depends()]):
    return _svc().get_list_rooms(params)


@router.get("/available")
def get_available_rooms(params: Annotated[AvailableRoomsParams, Depends()]):
    return _svc().get_available_rooms(params)


@router.get("/{id}")
def get_room(id: int):
    return _svc().get_room(id)


@router.post("")
def create_room(room: CreateRoom):
    return _svc().create_room(room)


@router.put("/{id}")
def update_room(id: int, room: UpdateRoom):
    return _svc().update_room(id, room)


@router.delete("/{id}")
def delete_room(id: int):
    return _svc().delete_room(id)

@router.post(f"/update-price")
def update_room_price(payload: UpdateRoomPrice):
    return _svc().update_room_price(payload)

@router.get("/get-history_prices/{id}")
def get_room_history_prices(id: int):
    return _svc().get_room_history_prices(id)