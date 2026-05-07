from fastapi import APIRouter
from src.db.db import db
from src.models.service_price_log import CreateServicePriceLog, UpdateServicePriceLog
from src.repositories.service_price_log_repo import ServicePriceLogRepository
from src.services.service_price_log_service import ServicePriceLogService

router = APIRouter(prefix="/api/service-price-logs", tags=["service-price-logs"])


def _svc() -> ServicePriceLogService:
    return ServicePriceLogService(ServicePriceLogRepository(db))


@router.get("")
def get_list_service_price_logs(page: int = 1, page_size: int = 10):
    return _svc().get_list_service_price_logs(page, page_size)


@router.get("/{id}")
def get_service_price_log(id: int):
    return _svc().get_service_price_log(id)


@router.post("")
def create_service_price_log(log: CreateServicePriceLog):
    return _svc().create_service_price_log(log)


@router.put("/{id}")
def update_service_price_log(id: int, log: UpdateServicePriceLog):
    return _svc().update_service_price_log(id, log)


@router.delete("/{id}")
def delete_service_price_log(id: int):
    return _svc().delete_service_price_log(id)
