from typing import Optional
from pydantic import BaseModel


class RoomType(BaseModel):
    id: int
    name: str
    is_deleted: bool

class CreateRoomType(BaseModel):
    name: str

class UpdateRoomType(BaseModel):
    name: Optional[str] = None
    is_deleted: Optional[bool] = None
