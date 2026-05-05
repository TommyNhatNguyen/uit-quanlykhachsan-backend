from fastapi import APIRouter
from src.db.db import db
from src.models.employee import CreateEmployee, UpdateEmployee
from src.repositories.employee_repo import EmployeeRepository
from src.services.employee_service import EmployeeService

router = APIRouter(prefix="/api/employees", tags=["employees"])


def _svc() -> EmployeeService:
    return EmployeeService(EmployeeRepository(db))


@router.get("")
def get_list_employees(page: int = 1, page_size: int = 10):
    return _svc().get_list_employees(page, page_size)


@router.get("/{employee_id}")
def get_employee(employee_id: int):
    return _svc().get_employee(employee_id)


@router.post("")
def create_employee(employee: CreateEmployee):
    return _svc().create_employee(employee)


@router.put("/{employee_id}")
def update_employee(employee_id: int, employee: UpdateEmployee):
    data = employee.model_dump()
    data["employee_id"] = employee_id
    return _svc().update_employee(UpdateEmployee(**data))


@router.delete("/{employee_id}")
def delete_employee(employee_id: int):
    return _svc().delete_employee(employee_id)
