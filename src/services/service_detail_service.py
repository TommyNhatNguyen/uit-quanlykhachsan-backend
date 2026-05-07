from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.service_detail import ServicesDetail, CreateServicesDetail, UpdateServicesDetail
from src.repositories.service_detail_repo import ServicesDetailRepository


class ServicesDetailService:
    def __init__(self, repo: ServicesDetailRepository):
        self.repo = repo

    def get_services_detail(self, id: int) -> ServicesDetail:
        result = self.repo.get_services_detail(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"ServicesDetail {id} not found")
        return result

    def get_list_services_details(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_services_details(page, page_size)

    def create_services_detail(self, detail: CreateServicesDetail) -> ServicesDetail:
        return self.repo.create_services_detail(detail)

    def update_services_detail(self, id: int, data: UpdateServicesDetail) -> ServicesDetail:
        current = self.repo.get_services_detail(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"ServicesDetail {id} not found")
        merged = {**current.model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_services_detail(id, ServicesDetail(**merged))

    def delete_services_detail(self, id: int) -> ServicesDetail:
        current = self.repo.get_services_detail(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"ServicesDetail {id} not found")
        self.repo.delete_services_detail(id)
        return current
