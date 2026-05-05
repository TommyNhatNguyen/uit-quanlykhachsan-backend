from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.models.payment_detail import PaymentDetail, CreatePaymentDetail, UpdatePaymentDetail
from src.models.paginate_model import PaginateModel
from src.repositories.payment_detail_repo import PaymentDetailRepository


class PaymentDetailService:
    def __init__(self, repo: PaymentDetailRepository):
        self.repo = repo

    def get_payment_detail(self, payment_detail_id: int) -> PaymentDetail:
        result = self.repo.get_payment_detail(payment_detail_id)
        if isinstance(result, JSONResponse):
            raise HTTPException(status_code=404, detail=f"PaymentDetail {payment_detail_id} not found")
        return result

    def get_list_payment_details(self, page: int = 1, page_size: int = 10) -> PaginateModel[PaymentDetail]:
        return self.repo.get_list_payment_details(page, page_size)

    def create_payment_detail(self, payment_detail: CreatePaymentDetail) -> PaymentDetail:
        return self.repo.create_payment_detail(payment_detail)

    def update_payment_detail(self, payment_detail: UpdatePaymentDetail) -> PaymentDetail:
        current = self.repo.get_payment_detail(payment_detail.payment_detail_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"PaymentDetail {payment_detail.payment_detail_id} not found")
        merged_data = current.model_dump()
        merged_data.update(payment_detail.model_dump(exclude_none=True))
        return self.repo.update_payment_detail(UpdatePaymentDetail(**merged_data))

    def delete_payment_detail(self, payment_detail_id: int) -> PaymentDetail:
        current = self.repo.get_payment_detail(payment_detail_id)
        if isinstance(current, JSONResponse):
            raise HTTPException(status_code=404, detail=f"PaymentDetail {payment_detail_id} not found")
        self.repo.delete_payment_detail(payment_detail_id)
        return current
