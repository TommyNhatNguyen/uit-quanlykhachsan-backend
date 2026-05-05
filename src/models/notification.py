from typing import Optional
from pydantic import BaseModel


class Notification(BaseModel):
    id: int
    title: str
    sub: Optional[str] = None
    time_str: Optional[str] = None
    unread: Optional[bool] = True
    icon: Optional[str] = "🔔"

class CreateNotification(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    sub: Optional[str] = None
    time_str: Optional[str] = None
    unread: Optional[bool] = True
    icon: Optional[str] = "🔔"

class UpdateNotification(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    sub: Optional[str] = None
    time_str: Optional[str] = None
    unread: Optional[bool] = None
    icon: Optional[str] = None
