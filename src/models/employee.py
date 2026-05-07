import enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from src.models.employee_account import EmployeeAccount
class Role(str, enum.Enum):
    staff = "staff"
    admin = "admin"
    accountant = "accountant"

class Employee(BaseModel):
    id: int
    name: str
    birthday: Optional[datetime]
    phone: int
    is_working: Optional[bool]
    position: Optional[str]
    start_working_date: datetime
    employee_account_id: Optional[int]
    is_deleted: bool
    role: Role


class PopulatedEmployee(Employee):
    employee_account: Optional[EmployeeAccount] = None

class CreateEmployee(BaseModel):
    name: str
    phone: int
    start_working_date: datetime

class UpdateEmployee(BaseModel):
    name: Optional[str] = None
    birthday: Optional[datetime] = None
    phone: Optional[int] = None
    is_working: Optional[bool] = None
    position: Optional[str] = None
    start_working_date: Optional[datetime] = None
    employee_account_id: Optional[int] = None
    is_deleted: Optional[bool] = None
    role: Optional[Role] = None