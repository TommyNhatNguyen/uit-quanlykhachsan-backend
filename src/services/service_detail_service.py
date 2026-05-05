from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.service_detail import ServiceDetail, CreateServiceDetail, UpdateServiceDetail
from src.repositories.service_detail_repo import ServiceDetailRepository


class ServiceDetailService:
    def __init__(self, repo: ServiceDetailRepository):
        self.repo = repo

    def get_service_detail(self, service_detail_id: int) -> ServiceDetail:
        result = self.repo.get_service_detail(service_detail_id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"ServiceDetail {service_detail_id} not found")
        return result

    def get_list_service_details(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_service_details(page, page_size)

    def create_service_detail(self, service_detail: CreateServiceDetail) -> ServiceDetail:
        return self.repo.create_service_detail(service_detail)

    def update_service_detail(self, service_detail: UpdateServiceDetail) -> ServiceDetail:
        current = self.repo.get_service_detail(service_detail.service_detail)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"ServiceDetail {service_detail.service_detail} not found")
        merged_data = current.model_dump()
        merged_data.update(service_detail.model_dump(exclude_none=True))
        return self.repo.update_service_detail(UpdateServiceDetail(**merged_data))

    def delete_service_detail(self, service_detail_id: int) -> ServiceDetail:
        current = self.repo.get_service_detail(service_detail_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"ServiceDetail {service_detail_id} not found")
        self.repo.delete_service_detail(service_detail_id)
        return current
