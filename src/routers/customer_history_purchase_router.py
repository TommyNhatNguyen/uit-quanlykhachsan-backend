from fastapi import APIRouter
from src.db.db import db
from src.models.customer_history_purchase import CreateCustomerHistoryPurchase, UpdateCustomerHistoryPurchase
from src.repositories.customer_history_purchase_repo import CustomerHistoryPurchaseRepository
from src.services.customer_history_purchase_service import CustomerHistoryPurchaseService

router = APIRouter(prefix="/api/customer-history-purchases", tags=["customer-history-purchases"])


def _svc() -> CustomerHistoryPurchaseService:
    return CustomerHistoryPurchaseService(CustomerHistoryPurchaseRepository(db))


@router.get("")
def get_list_customer_history_purchases(page: int = 1, page_size: int = 10):
    return _svc().get_list_customer_history_purchases(page, page_size)


@router.get("/{id}")
def get_customer_history_purchase(id: int):
    return _svc().get_customer_history_purchase(id)


@router.post("")
def create_customer_history_purchase(chp: CreateCustomerHistoryPurchase):
    return _svc().create_customer_history_purchase(chp)


@router.put("/{id}")
def update_customer_history_purchase(id: int, chp: UpdateCustomerHistoryPurchase):
    return _svc().update_customer_history_purchase(id, chp)


@router.delete("/{id}")
def delete_customer_history_purchase(id: int):
    return _svc().delete_customer_history_purchase(id)
