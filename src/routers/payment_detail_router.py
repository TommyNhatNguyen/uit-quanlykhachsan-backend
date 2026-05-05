from fastapi import APIRouter
from src.db.db import db
from src.models.payment_detail import CreatePaymentDetail, UpdatePaymentDetail
from src.repositories.payment_detail_repo import PaymentDetailRepository
from src.services.payment_detail_service import PaymentDetailService

router = APIRouter(prefix="/api/payment-details", tags=["payment-details"])


def _svc() -> PaymentDetailService:
    return PaymentDetailService(PaymentDetailRepository(db))


@router.get("")
def get_list_payment_details(page: int = 1, page_size: int = 10):
    return _svc().get_list_payment_details(page, page_size)


@router.get("/{payment_detail_id}")
def get_payment_detail(payment_detail_id: int):
    return _svc().get_payment_detail(payment_detail_id)


@router.post("")
def create_payment_detail(payment_detail: CreatePaymentDetail):
    return _svc().create_payment_detail(payment_detail)


@router.put("/{payment_detail_id}")
def update_payment_detail(payment_detail_id: int, payment_detail: UpdatePaymentDetail):
    data = payment_detail.model_dump()
    data["payment_detail_id"] = payment_detail_id
    return _svc().update_payment_detail(UpdatePaymentDetail(**data))


@router.delete("/{payment_detail_id}")
def delete_payment_detail(payment_detail_id: int):
    return _svc().delete_payment_detail(payment_detail_id)
