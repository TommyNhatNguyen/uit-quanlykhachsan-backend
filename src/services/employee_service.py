from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.employee import Employee, CreateEmployee, UpdateEmployee, LoginEmployee
from src.models.employee_account import CreateEmployeeAccount
from src.repositories.employee_repo import EmployeeRepository
from src.repositories.employee_account_repo import EmployeeAccountRepository


class EmployeeService:
    def __init__(self, repo: EmployeeRepository, account_repo: EmployeeAccountRepository):
        self.repo = repo
        self.account_repo = account_repo

    def get_employee(self, id: int) -> Employee:
        result = self.repo.get_employee(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Employee {id} not found")
        return result

    def get_list_employees(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_employees(page, page_size)

    def create_employee(self, data: CreateEmployee) -> Employee:
        account = self.account_repo.create_employee_account(
            CreateEmployeeAccount(
                username=data.username,
                password=data.password,
                created_at=datetime.now(),
            )
        )
        if isinstance(account, JSONResponse):
            raise HTTPException(status_code=500, detail="Failed to create employee account")

        result = self.repo.create_employee(data, employee_account_id=account.id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=500, detail="Failed to create employee")
        return result

    def update_employee(self, id: int, data: UpdateEmployee) -> Employee:
        current = self.repo.get_employee(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Employee {id} not found")
        merged = {**current.model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_employee(id, Employee(**merged))

    def login(self, data: LoginEmployee) -> Employee:
        account = self.account_repo.get_by_credentials(data.username, data.password)
        if not account or isinstance(account, JSONResponse):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        employee = self.repo.get_employee_by_account_id(account.id)
        if not employee or isinstance(employee, JSONResponse):
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee

    def delete_employee(self, id: int) -> Employee:
        current = self.repo.get_employee(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Employee {id} not found")
        self.repo.delete_employee(id)
        return current
