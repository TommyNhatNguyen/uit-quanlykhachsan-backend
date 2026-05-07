from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.service import Service, CreateService, UpdateService
from src.repositories.service_item_repo import ServiceRepository


class ServiceService:
    def __init__(self, repo: ServiceRepository):
        self.repo = repo

    def get_service(self, id: int) -> Service:
        result = self.repo.get_service(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Service {id} not found")
        return result

    def get_list_services(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_services(page, page_size)

    def create_service(self, service: CreateService) -> Service:
        return self.repo.create_service(service)

    def update_service(self, id: int, data: UpdateService) -> Service:
        current = self.repo.get_service(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Service {id} not found")
        merged = {**current.model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_service(id, Service(**merged))

    def delete_service(self, id: int) -> Service:
        current = self.repo.get_service(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Service {id} not found")
        self.repo.delete_service(id)
        return current
