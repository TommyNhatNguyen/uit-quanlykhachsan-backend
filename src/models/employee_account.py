from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from pydantic import BaseModel

if TYPE_CHECKING:
    from src.models.employee import Employee


class EmployeeAccount(BaseModel):
    id: int
    username: str
    password: str
    created_at: datetime


class PopulatedEmployeeAccount(EmployeeAccount):
    employee: Optional["Employee"] = None


class CreateEmployeeAccount(BaseModel):
    username: str
    password: str
    created_at: datetime = datetime.now()


class UpdateEmployeeAccount(BaseModel):
    password: Optional[str] = None
    created_at: Optional[datetime] = None
