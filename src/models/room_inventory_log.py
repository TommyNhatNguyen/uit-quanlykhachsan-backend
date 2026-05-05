from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class RoomInventoryLog(BaseModel):
    id: int
    room_id: Optional[int] = None
    room_number: Optional[str] = None
    room_type_id: Optional[int] = None
    is_available: Optional[float] = None
    created_at: Optional[datetime] = None

class CreateRoomInventoryLog(BaseModel):
    id: Optional[int] = None
    room_id: Optional[int] = None
    room_number: Optional[str] = None
    room_type_id: Optional[int] = None
    is_available: Optional[float] = None
    created_at: Optional[datetime] = None

class UpdateRoomInventoryLog(BaseModel):
    id: Optional[int] = None
    room_id: Optional[int] = None
    room_number: Optional[str] = None
    room_type_id: Optional[int] = None
    is_available: Optional[float] = None
    created_at: Optional[datetime] = None
