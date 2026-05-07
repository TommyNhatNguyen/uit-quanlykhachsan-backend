from fastapi import APIRouter
from src.db.db import db
from src.models.service import CreateServiceItem, UpdateServiceItem
from src.repositories.service_item_repo import ServiceItemRepository
from src.services.service_item_service import ServiceItemService

router = APIRouter(prefix="/api/service-items", tags=["service-items"])


def _svc() -> ServiceItemService:
    return ServiceItemService(ServiceItemRepository(db))


@router.get("")
def get_list_service_items(page: int = 1, page_size: int = 10):
    return _svc().get_list_service_items(page, page_size)


@router.get("/{service_item_id}")
def get_service_item(service_item_id: int):
    return _svc().get_service_item(service_item_id)


@router.post("")
def create_service_item(service_item: CreateServiceItem):
    return _svc().create_service_item(service_item)


@router.put("/{service_item_id}")
def update_service_item(service_item_id: int, service_item: UpdateServiceItem):
    data = service_item.model_dump()
    data["service_item_id"] = service_item_id
    return _svc().update_service_item(UpdateServiceItem(**data))


@router.delete("/{service_item_id}")
def delete_service_item(service_item_id: int):
    return _svc().delete_service_item(service_item_id)
