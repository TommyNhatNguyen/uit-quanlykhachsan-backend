from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.payment import Payment, CreatePayment, UpdatePayment, QueryPaymentsParams
from src.repositories.payment_repo import PaymentRepository


class PaymentService:
    def __init__(self, repo: PaymentRepository):
        self.repo = repo

    def get_payment(self, id: int) -> Payment:
        result = self.repo.get_payment(id)
        if not result or isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Payment {id} not found")
        return result

    def get_list_payments(self, params: QueryPaymentsParams) -> dict:
        return self.repo.get_list_payments(params)

    def create_payment(self, payment: CreatePayment) -> Payment:
        return self.repo.create_payment(payment)

    def update_payment(self, id: int, data: UpdatePayment) -> Payment:
        current = self.repo.get_payment(id)
        if not current or isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Payment {id} not found")
        merged = {**Payment(**current.model_dump()).model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_payment(id, Payment(**merged))

    def delete_payment(self, id: int) -> Payment:
        current = self.repo.get_payment(id)
        if not current or isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Payment {id} not found")
        self.repo.delete_payment(id)
        return current
