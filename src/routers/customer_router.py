from fastapi import APIRouter
from src.db.db import db
from src.models.customer import CreateCustomer, UpdateCustomer
from src.repositories.customer_repo import CustomerRepository
from src.services.customer_service import CustomerService

router = APIRouter(prefix="/api/customers", tags=["customers"])


def _svc() -> CustomerService:
    return CustomerService(CustomerRepository(db))


@router.get("")
def get_list_customers(page: int = 1, page_size: int = 10):
    return _svc().get_list_customers(page, page_size)


@router.get("/{customer_id}")
def get_customer(customer_id: int):
    return _svc().get_customer(customer_id)


@router.post("")
def create_customer(customer: CreateCustomer):
    return _svc().create_customer(customer)


@router.put("/{customer_id}")
def update_customer(customer_id: int, customer: UpdateCustomer):
    data = customer.model_dump()
    data["customer_id"] = customer_id
    return _svc().update_customer(UpdateCustomer(**data))


@router.delete("/{customer_id}")
def delete_customer(customer_id: int):
    return _svc().delete_customer(customer_id)
