from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.employee_account import EmployeeAccount, CreateEmployeeAccount, UpdateEmployeeAccount
from src.repositories.employee_account_repo import EmployeeAccountRepository


class EmployeeAccountService:
    def __init__(self, repo: EmployeeAccountRepository):
        self.repo = repo

    def get_employee_account(self, id: int) -> EmployeeAccount:
        result = self.repo.get_employee_account(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"EmployeeAccount {id} not found")
        return result

    def get_list_employee_accounts(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_employee_accounts(page, page_size)

    def create_employee_account(self, account: CreateEmployeeAccount) -> EmployeeAccount:
        return self.repo.create_employee_account(account)

    def update_employee_account(self, id: int, data: UpdateEmployeeAccount) -> EmployeeAccount:
        current = self.repo.get_employee_account(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"EmployeeAccount {id} not found")
        merged = {**current.model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_employee_account(id, EmployeeAccount(**merged))

    def delete_employee_account(self, id: int) -> EmployeeAccount:
        current = self.repo.get_employee_account(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"EmployeeAccount {id} not found")
        self.repo.delete_employee_account(id)
        return current
