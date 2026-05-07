from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from src.models.customer import Customer


class Membership(BaseModel):
    id: int
    name: str
    paid_from: Optional[float]
    paid_to: Optional[float]
    is_deleted: bool


class PopulatedMembership(Membership):
    customers: Optional[List["Customer"]] = None


class CreateMembership(BaseModel):
    name: str
    paid_from: Optional[float] = None
    paid_to: Optional[float] = None


class UpdateMembership(BaseModel):
    name: Optional[str] = None
    paid_from: Optional[float] = None
    paid_to: Optional[float] = None
    is_deleted: Optional[bool] = None
