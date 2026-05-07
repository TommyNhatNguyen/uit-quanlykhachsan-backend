from fastapi import APIRouter
from src.db.db import db
from src.models.room_type import CreateRoomType, UpdateRoomType
from src.repositories.room_type_repo import RoomTypeRepository
from src.services.room_type_service import RoomTypeService

router = APIRouter(prefix="/api/room-types", tags=["room-types"])


def _svc() -> RoomTypeService:
    return RoomTypeService(RoomTypeRepository(db))


@router.get("")
def get_list_room_types(page: int = 1, page_size: int = 10):
    return _svc().get_list_room_types(page, page_size)


@router.get("/{id}")
def get_room_type(id: int):
    return _svc().get_room_type(id)


@router.post("")
def create_room_type(room_type: CreateRoomType):
    return _svc().create_room_type(room_type)


@router.put("/{id}")
def update_room_type(id: int, room_type: UpdateRoomType):
    return _svc().update_room_type(id, room_type)


@router.delete("/{id}")
def delete_room_type(id: int):
    return _svc().delete_room_type(id)
