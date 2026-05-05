from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class RoomLogPrice(BaseModel):
    id: int
    room_id: Optional[int] = None
    using_form_datetime: Optional[datetime] = None
    using_to_datetime: Optional[datetime] = None
    price_per_night: Optional[float] = None

class CreateRoomLogPrice(BaseModel):
    id: Optional[int] = None
    room_id: Optional[int] = None
    using_form_datetime: Optional[datetime] = None
    using_to_datetime: Optional[datetime] = None
    price_per_night: Optional[float] = None

class UpdateRoomLogPrice(BaseModel):
    id: Optional[int] = None
    room_id: Optional[int] = None
    using_form_datetime: Optional[datetime] = None
    using_to_datetime: Optional[datetime] = None
    price_per_night: Optional[float] = None
