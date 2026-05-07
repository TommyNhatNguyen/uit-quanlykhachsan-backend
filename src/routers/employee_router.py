from fastapi import APIRouter
from src.db.db import db
from src.models.employee import CreateEmployee, UpdateEmployee, LoginEmployee
from src.repositories.employee_repo import EmployeeRepository
from src.repositories.employee_account_repo import EmployeeAccountRepository
from src.services.employee_service import EmployeeService

router = APIRouter(prefix="/api/employees", tags=["employees"])


def _svc() -> EmployeeService:
    return EmployeeService(EmployeeRepository(db), EmployeeAccountRepository(db))


@router.get("")
def get_list_employees(page: int = 1, page_size: int = 10):
    return _svc().get_list_employees(page, page_size)


@router.get("/{id}")
def get_employee(id: int):
    return _svc().get_employee(id)


@router.post("")
def create_employee(employee: CreateEmployee):
    return _svc().create_employee(employee)


@router.put("/{id}")
def update_employee(id: int, employee: UpdateEmployee):
    return _svc().update_employee(id, employee)


@router.delete("/{id}")
def delete_employee(id: int):
    return _svc().delete_employee(id)

@router.post("/login")
def login_employee(data: LoginEmployee):
    return _svc().login(data)