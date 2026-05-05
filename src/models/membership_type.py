from typing import Optional
from pydantic import BaseModel


class MembershipType(BaseModel):
    membership_type_id: int
    membership_type_name: Optional[str] = None
    paid_from: Optional[float] = None
    paid_to: Optional[float] = None

class CreateMembershipType(BaseModel):
    membership_type_id: Optional[int] = None
    membership_type_name: Optional[str] = None
    paid_from: Optional[float] = None
    paid_to: Optional[float] = None

class UpdateMembershipType(BaseModel):
    membership_type_id: Optional[int] = None
    membership_type_name: Optional[str] = None
    paid_from: Optional[float] = None
    paid_to: Optional[float] = None
