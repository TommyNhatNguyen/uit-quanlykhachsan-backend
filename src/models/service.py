from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from src.models.service_price_log import ServicePriceLog


class Service(BaseModel):
    id: int
    name: str
    catalog: Optional[str]
    current_price: float


class PopulatedService(Service):
    service_price_logs: Optional[List["ServicePriceLog"]] = None


class CreateService(BaseModel):
    name: str
    current_price: float = 0
    catalog: Optional[str] = None


class UpdateService(BaseModel):
    name: Optional[str] = None
    catalog: Optional[str] = None
    current_price: Optional[float] = None


class UpdateServicePrice(BaseModel):
    service_id: int
    price: float
