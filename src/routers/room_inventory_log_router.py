from fastapi import APIRouter
from src.db.db import db
from src.models.room_inventory_log import CreateRoomInventoryLog, UpdateRoomInventoryLog
from src.repositories.room_inventory_log_repo import RoomInventoryLogRepository
from src.services.room_inventory_log_service import RoomInventoryLogService

router = APIRouter(prefix="/api/room-inventory-logs", tags=["room-inventory-logs"])


def _svc() -> RoomInventoryLogService:
    return RoomInventoryLogService(RoomInventoryLogRepository(db))


@router.get("")
def get_list_room_inventory_logs(page: int = 1, page_size: int = 10):
    return _svc().get_list_room_inventory_logs(page, page_size)


@router.get("/{id}")
def get_room_inventory_log(id: int):
    return _svc().get_room_inventory_log(id)


@router.post("")
def create_room_inventory_log(log: CreateRoomInventoryLog):
    return _svc().create_room_inventory_log(log)


@router.put("/{id}")
def update_room_inventory_log(id: int, log: UpdateRoomInventoryLog):
    data = log.model_dump()
    data["id"] = id
    return _svc().update_room_inventory_log(UpdateRoomInventoryLog(**data))


@router.delete("/{id}")
def delete_room_inventory_log(id: int):
    return _svc().delete_room_inventory_log(id)
