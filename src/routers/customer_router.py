from typing import Annotated
from fastapi import APIRouter, Depends
from src.db.db import db
from src.models.customer import CreateCustomer, UpdateCustomer, QueryCustomersParams
from src.repositories.customer_repo import CustomerRepository
from src.services.customer_service import CustomerService

router = APIRouter(prefix="/api/customers", tags=["customers"])


def _svc() -> CustomerService:
    return CustomerService(CustomerRepository(db))


@router.get("")
def get_list_customers(params: Annotated[QueryCustomersParams, Depends()]):
    return _svc().get_list_customers(params)


@router.get("/{id}")
def get_customer(id: int):
    return _svc().get_customer(id)


@router.post("")
def create_customer(customer: CreateCustomer):
    return _svc().create_customer(customer)


@router.put("/{id}")
def update_customer(id: int, customer: UpdateCustomer):
    return _svc().update_customer(id, customer)


@router.delete("/{id}")
def delete_customer(id: int):
    return _svc().delete_customer(id)
