from typing import Annotated
from fastapi import APIRouter, Depends
from src.db.db import db
from src.models.payment import CreatePayment, UpdatePayment, QueryPaymentsParams
from src.repositories.payment_repo import PaymentRepository
from src.services.payment_service import PaymentService

router = APIRouter(prefix="/api/payments", tags=["payments"])


def _svc() -> PaymentService:
    return PaymentService(PaymentRepository(db))


@router.get("")
def get_list_payments(params: Annotated[QueryPaymentsParams, Depends()]):
    return _svc().get_list_payments(params)


@router.get("/{id}")
def get_payment(id: int):
    return _svc().get_payment(id)


@router.post("")
def create_payment(payment: CreatePayment):
    return _svc().create_payment(payment)


@router.put("/{id}")
def update_payment(id: int, payment: UpdatePayment):
    return _svc().update_payment(id, payment)


@router.delete("/{id}")
def delete_payment(id: int):
    return _svc().delete_payment(id)
