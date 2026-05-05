from typing import Optional
from pydantic import BaseModel


class Counter(BaseModel):
    name: str
    value: int = 0

class CreateCounter(BaseModel):
    name: Optional[str] = None
    value: Optional[int] = 0

class UpdateCounter(BaseModel):
    name: Optional[str] = None
    value: Optional[int] = None
