from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.service_price_log import ServicePriceLog, CreateServicePriceLog, UpdateServicePriceLog
from src.repositories.service_price_log_repo import ServicePriceLogRepository


class ServicePriceLogService:
    def __init__(self, repo: ServicePriceLogRepository):
        self.repo = repo

    def get_service_price_log(self, id: int) -> ServicePriceLog:
        result = self.repo.get_service_price_log(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"ServicePriceLog {id} not found")
        return result

    def get_list_service_price_logs(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_service_price_logs(page, page_size)

    def create_service_price_log(self, log: CreateServicePriceLog) -> ServicePriceLog:
        return self.repo.create_service_price_log(log)

    def update_service_price_log(self, id: int, data: UpdateServicePriceLog) -> ServicePriceLog:
        current = self.repo.get_service_price_log(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"ServicePriceLog {id} not found")
        merged = {**current.model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_service_price_log(id, ServicePriceLog(**merged))

    def delete_service_price_log(self, id: int) -> ServicePriceLog:
        current = self.repo.get_service_price_log(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"ServicePriceLog {id} not found")
        self.repo.delete_service_price_log(id)
        return current
