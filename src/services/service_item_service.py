from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.service import ServiceItem, CreateServiceItem, UpdateServiceItem
from src.repositories.service_item_repo import ServiceItemRepository


class ServiceItemService:
    def __init__(self, repo: ServiceItemRepository):
        self.repo = repo

    def get_service_item(self, service_item_id: int) -> ServiceItem:
        result = self.repo.get_service_item(service_item_id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"ServiceItem {service_item_id} not found")
        return result

    def get_list_service_items(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_service_items(page, page_size)

    def create_service_item(self, service_item: CreateServiceItem) -> ServiceItem:
        return self.repo.create_service_item(service_item)

    def update_service_item(self, service_item: UpdateServiceItem) -> ServiceItem:
        current = self.repo.get_service_item(service_item.service_item_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"ServiceItem {service_item.service_item_id} not found")
        merged_data = current.model_dump()
        merged_data.update(service_item.model_dump(exclude_none=True))
        return self.repo.update_service_item(UpdateServiceItem(**merged_data))

    def delete_service_item(self, service_item_id: int) -> ServiceItem:
        current = self.repo.get_service_item(service_item_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"ServiceItem {service_item_id} not found")
        self.repo.delete_service_item(service_item_id)
        return current
