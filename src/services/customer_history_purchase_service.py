from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.customer_history_purchase import CustomerHistoryPurchase, CreateCustomerHistoryPurchase, UpdateCustomerHistoryPurchase
from src.repositories.customer_history_purchase_repo import CustomerHistoryPurchaseRepository


class CustomerHistoryPurchaseService:
    def __init__(self, repo: CustomerHistoryPurchaseRepository):
        self.repo = repo

    def get_customer_history_purchase(self, id: int) -> CustomerHistoryPurchase:
        result = self.repo.get_customer_history_purchase(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"CustomerHistoryPurchase {id} not found")
        return result

    def get_list_customer_history_purchases(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_customer_history_purchases(page, page_size)

    def create_customer_history_purchase(self, chp: CreateCustomerHistoryPurchase) -> CustomerHistoryPurchase:
        return self.repo.create_customer_history_purchase(chp)

    def update_customer_history_purchase(self, id: int, data: UpdateCustomerHistoryPurchase) -> CustomerHistoryPurchase:
        current = self.repo.get_customer_history_purchase(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"CustomerHistoryPurchase {id} not found")
        merged = {**current.model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_customer_history_purchase(id, CustomerHistoryPurchase(**merged))

    def delete_customer_history_purchase(self, id: int) -> CustomerHistoryPurchase:
        current = self.repo.get_customer_history_purchase(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"CustomerHistoryPurchase {id} not found")
        self.repo.delete_customer_history_purchase(id)
        return current
