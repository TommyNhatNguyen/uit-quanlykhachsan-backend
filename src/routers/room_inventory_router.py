from fastapi import APIRouter
from src.db.db import db
from src.models.room_inventory import CreateRoomInventory, UpdateRoomInventory
from src.repositories.room_inventory_repo import RoomInventoryRepository
from src.services.room_inventory_service import RoomInventoryService

router = APIRouter(prefix="/api/room-inventories", tags=["room-inventories"])


def _svc() -> RoomInventoryService:
    return RoomInventoryService(RoomInventoryRepository(db))


@router.get("")
def get_list_room_inventories(page: int = 1, page_size: int = 10):
    return _svc().get_list_room_inventories(page, page_size)


@router.get("/{room_id}")
def get_room_inventory(room_id: int):
    return _svc().get_room_inventory(room_id)


@router.post("")
def create_room_inventory(room_inventory: CreateRoomInventory):
    return _svc().create_room_inventory(room_inventory)


@router.put("/{room_id}")
def update_room_inventory(room_id: int, room_inventory: UpdateRoomInventory):
    data = room_inventory.model_dump()
    data["room_id"] = room_id
    return _svc().update_room_inventory(UpdateRoomInventory(**data))


@router.delete("/{room_id}")
def delete_room_inventory(room_id: int):
    return _svc().delete_room_inventory(room_id)
