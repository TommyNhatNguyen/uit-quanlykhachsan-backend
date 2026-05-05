from fastapi import APIRouter
from src.db.db import db
from src.models.service_detail import CreateServiceDetail, UpdateServiceDetail
from src.repositories.service_detail_repo import ServiceDetailRepository
from src.services.service_detail_service import ServiceDetailService

router = APIRouter(prefix="/api/service-details", tags=["service-details"])


def _svc() -> ServiceDetailService:
    return ServiceDetailService(ServiceDetailRepository(db))


@router.get("")
def get_list_service_details(page: int = 1, page_size: int = 10):
    return _svc().get_list_service_details(page, page_size)


@router.get("/{service_detail_id}")
def get_service_detail(service_detail_id: int):
    return _svc().get_service_detail(service_detail_id)


@router.post("")
def create_service_detail(service_detail: CreateServiceDetail):
    return _svc().create_service_detail(service_detail)


@router.put("/{service_detail_id}")
def update_service_detail(service_detail_id: int, service_detail: UpdateServiceDetail):
    data = service_detail.model_dump()
    data["service_detail"] = service_detail_id
    return _svc().update_service_detail(UpdateServiceDetail(**data))


@router.delete("/{service_detail_id}")
def delete_service_detail(service_detail_id: int):
    return _svc().delete_service_detail(service_detail_id)
