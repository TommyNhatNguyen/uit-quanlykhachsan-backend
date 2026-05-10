from fastapi import APIRouter
from src.db.db import db
from src.models.service import CreateService, UpdateService, UpdateServicePrice
from src.repositories.service_item_repo import ServiceRepository
from src.repositories.service_price_log_repo import ServicePriceLogRepository
from src.services.service_item_service import ServiceService
from src.services.service_price_log_service import ServicePriceLogService

router = APIRouter(prefix="/api/services", tags=["services"])


def _svc() -> ServiceService:
    return ServiceService(
        ServiceRepository(db),
        price_log_service=ServicePriceLogService(ServicePriceLogRepository(db))
    )


@router.get("")
def get_list_services(page: int = 1, page_size: int = 10):
    return _svc().get_list_services(page, page_size)


@router.get("/{id}")
def get_service(id: int):
    return _svc().get_service(id)


@router.post("")
def create_service(service: CreateService):
    return _svc().create_service(service)


@router.put("/{id}")
def update_service(id: int, service: UpdateService):
    return _svc().update_service(id, service)


@router.delete("/{id}")
def delete_service(id: int):
    return _svc().delete_service(id)


@router.post("/update-price")
def update_service_price(payload: UpdateServicePrice):
    return _svc().update_service_price(payload)


@router.get("/get-history-prices/{id}")
def get_service_history_prices(id: int):
    return _svc().get_service_history_prices(id)
