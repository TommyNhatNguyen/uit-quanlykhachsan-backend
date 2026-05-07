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
