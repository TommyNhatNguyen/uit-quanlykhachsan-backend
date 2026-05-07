from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from src.models.room import Room


class RoomPriceLog(BaseModel):
    id: int
    room_id: int
    created_at: Optional[datetime]
    price_per_night: float


class PopulatedRoomPriceLog(RoomPriceLog):
    room: Optional[Room] = None


class CreateRoomPriceLog(BaseModel):
    room_id: int
    price_per_night: float
    created_at: datetime = datetime.now()


class UpdateRoomPriceLog(BaseModel):
    room_id: Optional[int] = None
    created_at: Optional[datetime] = None
    price_per_night: Optional[float] = None
