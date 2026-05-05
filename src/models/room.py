from typing import Optional
from pydantic import BaseModel


class Room(BaseModel):
    room_id: int
    room_number: Optional[str] = None
    room_type_id: Optional[int] = None
    price_per_night: Optional[float] = None
    capacity: Optional[str] = None
    room_area: Optional[str] = None
    is_smoking: Optional[bool] = None
    description: Optional[str] = None

class CreateRoom(BaseModel):
    room_id: Optional[int] = None
    room_number: Optional[str] = None
    room_type_id: Optional[int] = None
    price_per_night: Optional[float] = None
    capacity: Optional[str] = None
    room_area: Optional[str] = None
    is_smoking: Optional[bool] = None
    description: Optional[str] = None

class UpdateRoom(BaseModel):
    room_id: Optional[int] = None
    room_number: Optional[str] = None
    room_type_id: Optional[int] = None
    price_per_night: Optional[float] = None
    capacity: Optional[str] = None
    room_area: Optional[str] = None
    is_smoking: Optional[bool] = None
    description: Optional[str] = None
