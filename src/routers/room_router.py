from typing import Annotated
from fastapi import APIRouter, Depends
from src.db.db import db
from src.models.room import CreateRoom, QueryRoomsParams, UpdateRoom
from src.repositories.room_repo import RoomRepository
from src.services.room_service import RoomService

router = APIRouter(prefix="/api/rooms", tags=["rooms"])


def _svc() -> RoomService:
    return RoomService(RoomRepository(db))


@router.get("")
def get_list_rooms(params: Annotated[QueryRoomsParams, Depends()]):
    return _svc().get_list_rooms(params)


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
