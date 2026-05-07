from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from src.models.service import Service


class ServicePriceLog(BaseModel):
    id: int
    service_id: int
    created_at: Optional[datetime]
    price: float


class PopulatedServicePriceLog(ServicePriceLog):
    service: Optional[Service] = None


class CreateServicePriceLog(BaseModel):
    service_id: int
    price: float
    created_at: datetime = datetime.now()


class UpdateServicePriceLog(BaseModel):
    service_id: Optional[int] = None
    created_at: Optional[datetime] = None
    price: Optional[float] = None