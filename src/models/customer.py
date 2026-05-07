from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from src.models.membership import Membership

class Customer(BaseModel):
    id: int
    name: str
    phone: int
    # 1: Nam, 2: Nữ, 3: Khác
    sex: int 
    identification_id: str
    email: Optional[str]
    birthday: Optional[datetime]
    membership_type_id: Optional[int]


class PopulatedCustomer(Customer):
    membership_type: Optional[Membership] = None

class CreateCustomer(BaseModel):
    name: str
    phone: int
    sex: int
    identification_id: str
    email: Optional[str] = None
    birthday: Optional[datetime] = None
    membership_type_id: Optional[int] = None


class UpdateCustomer(BaseModel):
    name: Optional[str] = None
    phone: Optional[int] = None
    sex: Optional[int] = None
    email: Optional[str] = None
    birthday: Optional[datetime] = None
    identification_id: Optional[str] = None
    membership_type_id: Optional[int] = None