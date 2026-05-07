from typing import Optional
from pydantic import BaseModel

class Hotel(BaseModel):
    id: int
    name: str
    address: str
    phone: str
    is_deleted: bool 

class CreateHotel(BaseModel):
    name: str
    address: str
    phone: str

class UpdateHotel(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    is_deleted: Optional[bool] = None