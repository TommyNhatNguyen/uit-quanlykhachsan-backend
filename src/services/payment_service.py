from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.payment import Payment, CreatePayment, UpdatePayment
from src.repositories.payment_repo import PaymentRepository


class PaymentService:
    def __init__(self, repo: PaymentRepository):
        self.repo = repo

    def get_payment(self, id: int) -> Payment:
        result = self.repo.get_payment(id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Payment {id} not found")
        return result

    def get_list_payments(self, page: int = 1, page_size: int = 10) -> dict:
        return self.repo.get_list_payments(page, page_size)

    def create_payment(self, payment: CreatePayment) -> Payment:
        return self.repo.create_payment(payment)

    def update_payment(self, id: int, data: UpdatePayment) -> Payment:
        current = self.repo.get_payment(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Payment {id} not found")
        merged = {**current.model_dump(), **data.model_dump(exclude_none=True)}
        return self.repo.update_payment(id, Payment(**merged))

    def delete_payment(self, id: int) -> Payment:
        current = self.repo.get_payment(id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Payment {id} not found")
        self.repo.delete_payment(id)
        return current
