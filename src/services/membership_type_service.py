from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.membership_type import MembershipType, CreateMembershipType, UpdateMembershipType
from src.repositories.membership_type_repo import MembershipTypeRepository


class MembershipTypeService:
    def __init__(self, repo: MembershipTypeRepository):
        self.repo = repo

    def get_membership_type(self, membership_type_id: int) -> MembershipType:
        result = self.repo.get_membership_type(membership_type_id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"MembershipType {membership_type_id} not found")
        return result

    def get_list_membership_types(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_membership_types(page, page_size)

    def create_membership_type(self, membership_type: CreateMembershipType) -> MembershipType:
        return self.repo.create_membership_type(membership_type)

    def update_membership_type(self, membership_type: UpdateMembershipType) -> MembershipType:
        current = self.repo.get_membership_type(membership_type.membership_type_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"MembershipType {membership_type.membership_type_id} not found")
        merged_data = current.model_dump()
        merged_data.update(membership_type.model_dump(exclude_none=True))
        return self.repo.update_membership_type(UpdateMembershipType(**merged_data))

    def delete_membership_type(self, membership_type_id: int) -> MembershipType:
        current = self.repo.get_membership_type(membership_type_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"MembershipType {membership_type_id} not found")
        self.repo.delete_membership_type(membership_type_id)
        return current
