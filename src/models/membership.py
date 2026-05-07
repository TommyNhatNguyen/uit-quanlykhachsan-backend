from typing import Optional
from pydantic import BaseModel


class Membership(BaseModel):
    id: int
    name: str
    paid_from: Optional[float]
    paid_to: Optional[float]
    is_deleted: bool


class CreateMembership(BaseModel):
    name: str
    paid_from: Optional[float] = None
    paid_to: Optional[float] = None


class UpdateMembership(BaseModel):
    name: Optional[str] = None
    paid_from: Optional[float] = None
    paid_to: Optional[float] = None
    is_deleted: Optional[bool] = None