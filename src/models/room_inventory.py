from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class RoomInventory(BaseModel):
    room_id: int
    room_number: Optional[str] = None
    room_type_id: Optional[int] = None
    is_available: Optional[float] = None
    updated_at: Optional[datetime] = None

class CreateRoomInventory(BaseModel):
    room_id: Optional[int] = None
    room_number: Optional[str] = None
    room_type_id: Optional[int] = None
    is_available: Optional[float] = None
    updated_at: Optional[datetime] = None

class UpdateRoomInventory(BaseModel):
    room_id: Optional[int] = None
    room_number: Optional[str] = None
    room_type_id: Optional[int] = None
    is_available: Optional[float] = None
    updated_at: Optional[datetime] = None
