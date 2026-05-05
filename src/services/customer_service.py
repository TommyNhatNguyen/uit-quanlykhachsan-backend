from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.customer import Customer, CreateCustomer, UpdateCustomer
from src.models.paginate_model import PaginateModel
from src.repositories.customer_repo import CustomerRepository


class CustomerService:
    def __init__(self, repo: CustomerRepository):
        self.repo = repo

    def get_customer(self, customer_id: int) -> Customer:
        result = self.repo.get_customer(customer_id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
        return result

    def get_list_customers(self, page: int = 1, page_size: int = 10) -> PaginateModel[Customer]:
        return self.repo.get_list_customers(page, page_size)

    def create_customer(self, customer: CreateCustomer) -> Customer:
        return self.repo.create_customer(customer)

    def update_customer(self, customer: UpdateCustomer) -> Customer:
        current = self.repo.get_customer(customer.customer_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Customer {customer.customer_id} not found")
        merged_data = current.model_dump()
        merged_data.update(customer.model_dump(exclude_none=True))
        return self.repo.update_customer(UpdateCustomer(**merged_data))

    def delete_customer(self, customer_id: int) -> Customer:
        current = self.repo.get_customer(customer_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
        self.repo.delete_customer(customer_id)
        return current
