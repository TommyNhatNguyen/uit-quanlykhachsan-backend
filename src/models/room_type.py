from typing import Optional
from pydantic import BaseModel


class RoomType(BaseModel):
    room_type_id: int
    room_type_name: Optional[str] = None

class CreateRoomType(BaseModel):
    room_type_id: Optional[int] = None
    room_type_name: Optional[str] = None

class UpdateRoomType(BaseModel):
    room_type_id: Optional[int] = None
    room_type_name: Optional[str] = None
