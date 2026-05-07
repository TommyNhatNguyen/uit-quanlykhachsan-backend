from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.employee import Employee, CreateEmployee, UpdateEmployee
from src.repositories.employee_repo import EmployeeRepository


class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

    def get_employee(self, id: int) -> Employee:
        result = self.repo.get_employee(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Employee {id} not found")
        return result

    def get_list_employees(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_employees(page, page_size)

    def create_employee(self, employee: CreateEmployee) -> Employee:
        return self.repo.create_employee(employee)

    def update_employee(self, id: int, data: UpdateEmployee) -> Employee:
        current = self.repo.get_employee(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Employee {id} not found")
        merged = {**current.model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_employee(id, Employee(**merged))

    def delete_employee(self, id: int) -> Employee:
        current = self.repo.get_employee(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Employee {id} not found")
        self.repo.delete_employee(id)
        return current
