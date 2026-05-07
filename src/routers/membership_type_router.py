from fastapi import APIRouter
from src.db.db import db
from src.models.membership import CreateMembershipType, UpdateMembershipType
from src.repositories.membership_type_repo import MembershipTypeRepository
from src.services.membership_type_service import MembershipTypeService

router = APIRouter(prefix="/api/membership-types", tags=["membership-types"])


def _svc() -> MembershipTypeService:
    return MembershipTypeService(MembershipTypeRepository(db))


@router.get("")
def get_list_membership_types(page: int = 1, page_size: int = 10):
    return _svc().get_list_membership_types(page, page_size)


@router.get("/{membership_type_id}")
def get_membership_type(membership_type_id: int):
    return _svc().get_membership_type(membership_type_id)


@router.post("")
def create_membership_type(membership_type: CreateMembershipType):
    return _svc().create_membership_type(membership_type)


@router.put("/{membership_type_id}")
def update_membership_type(membership_type_id: int, membership_type: UpdateMembershipType):
    data = membership_type.model_dump()
    data["membership_type_id"] = membership_type_id
    return _svc().update_membership_type(UpdateMembershipType(**data))


@router.delete("/{membership_type_id}")
def delete_membership_type(membership_type_id: int):
    return _svc().delete_membership_type(membership_type_id)
