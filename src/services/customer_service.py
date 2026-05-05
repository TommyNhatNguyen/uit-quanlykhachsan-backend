from src.models.customer import CreateCustomer, Customer
from src.repositories.api_state import ApiStateRepository


class CustomerService:
    def __init__(self, repo: ApiStateRepository):
        self.repo = repo

    async def create_customer(self, customer: CreateCustomer) -> Customer:
        return await self.repo.create_customer(customer)

    async def get_customers(self) -> list[Customer]:
        return await self.repo.get_state()