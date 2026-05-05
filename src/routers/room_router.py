from fastapi import APIRouter
from src.db.db import db
from src.models.room import CreateRoom, UpdateRoom
from src.repositories.room_repo import RoomRepository
from src.services.room_service import RoomService

router = APIRouter(prefix="/api/rooms", tags=["rooms"])


def _svc() -> RoomService:
    return RoomService(RoomRepository(db))


@router.get("")
def get_list_rooms(page: int = 1, page_size: int = 10):
    return _svc().get_list_rooms(page, page_size)


@router.get("/{room_id}")
def get_room(room_id: int):
    return _svc().get_room(room_id)


@router.post("")
def create_room(room: CreateRoom):
    return _svc().create_room(room)


@router.put("/{room_id}")
def update_room(room_id: int, room: UpdateRoom):
    data = room.model_dump()
    data["room_id"] = room_id
    return _svc().update_room(UpdateRoom(**data))


@router.delete("/{room_id}")
def delete_room(room_id: int):
    return _svc().delete_room(room_id)
