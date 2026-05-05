from typing import Optional
from pydantic import BaseModel


class ServiceItem(BaseModel):
    service_item_id: int
    service_item_name: Optional[str] = None
    catalog: Optional[str] = None
    price: Optional[float] = None
    used_count: Optional[int] = 0

class CreateServiceItem(BaseModel):
    service_item_id: Optional[int] = None
    service_item_name: Optional[str] = None
    catalog: Optional[str] = None
    price: Optional[float] = None
    used_count: Optional[int] = 0

class UpdateServiceItem(BaseModel):
    service_item_id: Optional[int] = None
    service_item_name: Optional[str] = None
    catalog: Optional[str] = None
    price: Optional[float] = None
    used_count: Optional[int] = None
