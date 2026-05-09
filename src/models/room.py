from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING, Tuple
from pydantic import BaseModel

from src.models.hotel import Hotel
from src.models.room_type import RoomType

if TYPE_CHECKING:
    from src.models.room_price_log import RoomPriceLog


class Room(BaseModel):
    id: int
    room_num: str
    room_name: str
    capacity: int
    area: float
    is_smoking: Optional[bool]
    has_wifi: Optional[bool]
    has_pool: Optional[bool]
    description: Optional[str]
    room_type_id: Optional[int]
    hotel_id: Optional[int]
    current_price_per_night: float
    is_deleted: bool
    is_underconstruction: Optional[bool]


class PopulatedRoom(Room):
    room_type: Optional[RoomType] = None
    hotel: Optional[Hotel] = None
    room_price_logs: Optional[List["RoomPriceLog"]] = None


class CreateRoom(BaseModel):
    room_num: str
    room_name: str
    capacity: int
    area: float
    current_price_per_night: float
    is_smoking: Optional[bool] = None
    has_wifi: Optional[bool] = None
    has_pool: Optional[bool] = None
    description: Optional[str] = None
    room_type_id: Optional[int] = None
    hotel_id: Optional[int] = None
    is_underconstruction: Optional[bool] = None


class UpdateRoom(BaseModel):
    room_num: Optional[str] = None
    room_name: Optional[str] = None
    capacity: Optional[int] = None
    area: Optional[float] = None
    is_smoking: Optional[bool] = None
    has_wifi: Optional[bool] = None
    has_pool: Optional[bool] = None
    description: Optional[str] = None
    room_type_id: Optional[int] = None
    hotel_id: Optional[int] = None
    current_price_per_night: Optional[float] = None
    is_deleted: Optional[bool] = None
    is_underconstruction: Optional[bool] = None

class UpdateRoomPrice(BaseModel):
    room_id: int
    price_per_night: float

class QueryRoomsParams(BaseModel):
    page: int = 1
    page_size: int = 10
    room_type_id: Optional[int] = None
    price_from: Optional[float] = None
    price_to: Optional[float] = None