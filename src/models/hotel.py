from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from src.models.room import Room


class Hotel(BaseModel):
    id: int
    name: str
    address: str
    phone: str
    is_deleted: bool


class PopulatedHotel(Hotel):
    rooms: Optional[List["Room"]] = None


class CreateHotel(BaseModel):
    name: str
    address: str
    phone: str


class UpdateHotel(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    is_deleted: Optional[bool] = None
