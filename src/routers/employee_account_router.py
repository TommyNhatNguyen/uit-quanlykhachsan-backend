from fastapi import APIRouter
from src.db.db import db
from src.models.employee_account import CreateEmployeeAccount, UpdateEmployeeAccount
from src.repositories.employee_account_repo import EmployeeAccountRepository
from src.services.employee_account_service import EmployeeAccountService

router = APIRouter(prefix="/api/employee-accounts", tags=["employee-accounts"])


def _svc() -> EmployeeAccountService:
    return EmployeeAccountService(EmployeeAccountRepository(db))


@router.get("")
def get_list_employee_accounts(page: int = 1, page_size: int = 10):
    return _svc().get_list_employee_accounts(page, page_size)


@router.get("/{id}")
def get_employee_account(id: int):
    return _svc().get_employee_account(id)


@router.post("")
def create_employee_account(account: CreateEmployeeAccount):
    return _svc().create_employee_account(account)


@router.put("/{id}")
def update_employee_account(id: int, account: UpdateEmployeeAccount):
    return _svc().update_employee_account(id, account)


@router.delete("/{id}")
def delete_employee_account(id: int):
    return _svc().delete_employee_account(id)
