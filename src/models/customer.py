from typing import Optional
from pydantic import BaseModel
from datetime import date

class Customer(BaseModel):
    customer_id: int
    customer_name: str
    sex: str
    phone: str
    email: str
    birthday: Optional[date] = None
    membership_type_id: int
    total_paid: float
    notes: Optional[str] = None
    created_at: Optional[date] = None
    updated_at: Optional[date] = None

class CreateCustomer(BaseModel):
    customer_id: Optional[int] = None
    customer_name: Optional[str] = None
    sex: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    birthday: Optional[date] = None
    membership_type_id: Optional[int] = None
    total_paid: Optional[float] = None

class UpdateCustomer(BaseModel):
    customer_id: Optional[int] = None
    customer_name: Optional[str] = None
    sex: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    birthday: Optional[date] = None
    membership_type_id: Optional[int] = None
    total_paid: Optional[float] = None