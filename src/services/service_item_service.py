from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.service import Service, CreateService, UpdateService, UpdateServicePrice
from src.models.service_price_log import CreateServicePriceLog
from src.repositories.service_item_repo import ServiceRepository
from src.services.service_price_log_service import ServicePriceLogService
from datetime import datetime


class ServiceService:
    def __init__(self, repo: ServiceRepository, price_log_service: ServicePriceLogService):
        self.repo = repo
        self.price_log_service = price_log_service

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

    def update_service_price(self, payload: UpdateServicePrice) -> Service:
        current = self.repo.get_service(payload.service_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Service {payload.service_id} not found")
        merged = {**current.model_dump(), **UpdateService(current_price=payload.price).model_dump(exclude_none=True)}
        result = self.repo.update_service(payload.service_id, Service(**merged))
        self.price_log_service.create_service_price_log(CreateServicePriceLog(
            service_id=payload.service_id,
            price=payload.price,
            created_at=datetime.now(),
        ))
        return result

    def get_service_history_prices(self, id: int):
        return self.repo.get_service_history_prices(id)
