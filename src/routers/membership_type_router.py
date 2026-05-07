from fastapi import APIRouter
from src.db.db import db
from src.models.membership import CreateMembership, UpdateMembership
from src.repositories.membership_type_repo import MembershipRepository
from src.services.membership_type_service import MembershipService

router = APIRouter(prefix="/api/memberships", tags=["memberships"])


def _svc() -> MembershipService:
    return MembershipService(MembershipRepository(db))


@router.get("")
def get_list_memberships(page: int = 1, page_size: int = 10):
    return _svc().get_list_memberships(page, page_size)


@router.get("/{id}")
def get_membership(id: int):
    return _svc().get_membership(id)


@router.post("")
def create_membership(membership: CreateMembership):
    return _svc().create_membership(membership)


@router.put("/{id}")
def update_membership(id: int, membership: UpdateMembership):
    return _svc().update_membership(id, membership)


@router.delete("/{id}")
def delete_membership(id: int):
    return _svc().delete_membership(id)
