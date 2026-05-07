from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class EmployeeAccount(BaseModel):
    id: int
    username: str
    password: str
    created_at: datetime

class CreateEmployeeAccount(BaseModel):
    username: str
    password: str
    created_at: datetime = datetime.now()

class UpdateEmployeeAccount(BaseModel):
    password: Optional[str] = None
    created_at: Optional[datetime] = None