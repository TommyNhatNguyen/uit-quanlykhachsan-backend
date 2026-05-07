from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from src.models.room import Room


class RoomType(BaseModel):
    id: int
    name: str
    is_deleted: bool


class PopulatedRoomType(RoomType):
    rooms: Optional[List["Room"]] = None


class CreateRoomType(BaseModel):
    name: str


class UpdateRoomType(BaseModel):
    name: Optional[str] = None
    is_deleted: Optional[bool] = None
