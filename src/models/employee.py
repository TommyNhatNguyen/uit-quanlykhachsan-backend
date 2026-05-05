from typing import Optional
from datetime import date
from pydantic import BaseModel


class Employee(BaseModel):
    employee_id: int
    employee_name: Optional[str] = None
    birthday: Optional[date] = None
    phone: Optional[str] = None
    is_working: Optional[str] = None
    position: Optional[str] = None
    start_working_date: Optional[date] = None

class CreateEmployee(BaseModel):
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    birthday: Optional[date] = None
    phone: Optional[str] = None
    is_working: Optional[str] = None
    position: Optional[str] = None
    start_working_date: Optional[date] = None

class UpdateEmployee(BaseModel):
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    birthday: Optional[date] = None
    phone: Optional[str] = None
    is_working: Optional[str] = None
    position: Optional[str] = None
    start_working_date: Optional[date] = None
