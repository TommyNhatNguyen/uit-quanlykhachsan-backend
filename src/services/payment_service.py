from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.payment import Payment, CreatePayment, UpdatePayment
from src.models.paginate_model import PaginateModel
from src.repositories.payment_repo import PaymentRepository


class PaymentService:
    def __init__(self, repo: PaymentRepository):
        self.repo = repo

    def get_payment(self, payment_id: int) -> Payment:
        result = self.repo.get_payment(payment_id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Payment {payment_id} not found")
        return result

    def get_list_payments(self, page: int = 1, page_size: int = 10) -> PaginateModel[Payment]:
        return self.repo.get_list_payments(page, page_size)

    def create_payment(self, payment: CreatePayment) -> Payment:
        return self.repo.create_payment(payment)

    def update_payment(self, payment: UpdatePayment) -> Payment:
        current = self.repo.get_payment(payment.payment_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Payment {payment.payment_id} not found")
        merged_data = current.model_dump()
        merged_data.update(payment.model_dump(exclude_none=True))
        return self.repo.update_payment(UpdatePayment(**merged_data))

    def delete_payment(self, payment_id: int) -> Payment:
        current = self.repo.get_payment(payment_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"Payment {payment_id} not found")
        self.repo.delete_payment(payment_id)
        return current
