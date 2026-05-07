from typing import Annotated
from fastapi import APIRouter, Depends
from src.db.db import db
from src.models.room_price_log import CreateRoomPriceLog, QueryRoomPriceLogsParams, UpdateRoomPriceLog
from src.repositories.room_log_price_repo import RoomPriceLogRepository
from src.services.room_log_price_service import RoomPriceLogService

router = APIRouter(prefix="/api/room-price-logs", tags=["room-price-logs"])


def _svc() -> RoomPriceLogService:
    return RoomPriceLogService(RoomPriceLogRepository(db))


@router.get("")
def get_list_room_price_logs(params: Annotated[QueryRoomPriceLogsParams, Depends()]):
    return _svc().get_list_room_price_logs(params)


@router.get("/{id}")
def get_room_price_log(id: int):
    return _svc().get_room_price_log(id)


@router.post("")
def create_room_price_log(log: CreateRoomPriceLog):
    return _svc().create_room_price_log(log)


@router.put("/{id}")
def update_room_price_log(id: int, log: UpdateRoomPriceLog):
    return _svc().update_room_price_log(id, log)


@router.delete("/{id}")
def delete_room_price_log(id: int):
    return _svc().delete_room_price_log(id)
