from fastapi import APIRouter
from src.db.db import db
from src.models.service_detail import CreateServicesDetail, UpdateServicesDetail
from src.repositories.service_detail_repo import ServicesDetailRepository
from src.services.service_detail_service import ServicesDetailService

router = APIRouter(prefix="/api/service-details", tags=["service-details"])


def _svc() -> ServicesDetailService:
    return ServicesDetailService(ServicesDetailRepository(db))


@router.get("")
def get_list_services_details(page: int = 1, page_size: int = 10):
    return _svc().get_list_services_details(page, page_size)


@router.get("/{id}")
def get_services_detail(id: int):
    return _svc().get_services_detail(id)


@router.post("")
def create_services_detail(detail: CreateServicesDetail):
    return _svc().create_services_detail(detail)


@router.put("/{id}")
def update_services_detail(id: int, detail: UpdateServicesDetail):
    return _svc().update_services_detail(id, detail)


@router.delete("/{id}")
def delete_services_detail(id: int):
    return _svc().delete_services_detail(id)
