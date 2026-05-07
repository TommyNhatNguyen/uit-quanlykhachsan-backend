from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.customer import Customer, CreateCustomer, UpdateCustomer
from src.repositories.customer_repo import CustomerRepository


class CustomerService:
    def __init__(self, repo: CustomerRepository):
        self.repo = repo

    def get_customer(self, id: int) -> Customer:
        result = self.repo.get_customer(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Customer {id} not found")
        return result

    def get_list_customers(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_customers(page, page_size)

    def create_customer(self, customer: CreateCustomer) -> Customer:
        return self.repo.create_customer(customer)

    def update_customer(self, id: int, data: UpdateCustomer) -> Customer:
        current = self.repo.get_customer(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Customer {id} not found")
        merged = {**current.model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_customer(id, Customer(**merged))

    def delete_customer(self, id: int) -> Customer:
        current = self.repo.get_customer(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Customer {id} not found")
        self.repo.delete_customer(id)
        return current
