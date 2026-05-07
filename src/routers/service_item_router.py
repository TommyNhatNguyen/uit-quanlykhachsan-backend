from fastapi import APIRouter
from src.db.db import db
from src.models.service import CreateService, UpdateService
from src.repositories.service_item_repo import ServiceRepository
from src.services.service_item_service import ServiceService

router = APIRouter(prefix="/api/services", tags=["services"])


def _svc() -> ServiceService:
    return ServiceService(ServiceRepository(db))


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
