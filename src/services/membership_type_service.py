from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.membership import Membership, CreateMembership, UpdateMembership
from src.repositories.membership_type_repo import MembershipRepository


class MembershipService:
    def __init__(self, repo: MembershipRepository):
        self.repo = repo

    def get_membership(self, id: int) -> Membership:
        result = self.repo.get_membership(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Membership {id} not found")
        return result

    def get_list_memberships(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_memberships(page, page_size)

    def create_membership(self, membership: CreateMembership) -> Membership:
        return self.repo.create_membership(membership)

    def update_membership(self, id: int, data: UpdateMembership) -> Membership:
        current = self.repo.get_membership(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Membership {id} not found")
        merged = {**current.model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_membership(id, Membership(**merged))

    def delete_membership(self, id: int) -> Membership:
        current = self.repo.get_membership(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Membership {id} not found")
        self.repo.delete_membership(id)
        return current
