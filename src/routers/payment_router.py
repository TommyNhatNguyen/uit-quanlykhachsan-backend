from fastapi import APIRouter
from src.db.db import db
from src.models.payment import CreatePayment, UpdatePayment
from src.repositories.payment_repo import PaymentRepository
from src.services.payment_service import PaymentService

router = APIRouter(prefix="/api/payments", tags=["payments"])


def _svc() -> PaymentService:
    return PaymentService(PaymentRepository(db))


@router.get("")
def get_list_payments(page: int = 1, page_size: int = 10):
    return _svc().get_list_payments(page, page_size)


@router.get("/{payment_id}")
def get_payment(payment_id: int):
    return _svc().get_payment(payment_id)


@router.post("")
def create_payment(payment: CreatePayment):
    return _svc().create_payment(payment)


@router.put("/{payment_id}")
def update_payment(payment_id: int, payment: UpdatePayment):
    data = payment.model_dump()
    data["payment_id"] = payment_id
    return _svc().update_payment(UpdatePayment(**data))


@router.delete("/{payment_id}")
def delete_payment(payment_id: int):
    return _svc().delete_payment(payment_id)
