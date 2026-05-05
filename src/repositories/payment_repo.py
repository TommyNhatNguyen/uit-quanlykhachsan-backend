import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.payment import Payment, CreatePayment, UpdatePayment
from src.models.paginate_model import PaginateModel


class PaymentRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_payment(self, payment: CreatePayment) -> Payment:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.payment (payment_id, status) VALUES (%s, %s)
            """, (payment.payment_id, payment.status))
            conn.commit()
            return self.get_payment(payment.payment_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_payment(self, payment_id: int) -> Payment:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.payment WHERE payment_id = %s
            """, (payment_id,))
            return Payment(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_payment(self, payment: UpdatePayment) -> Payment:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.payment SET status = %s WHERE payment_id = %s
            """, (payment.status, payment.payment_id))
            conn.commit()
            return self.get_payment(payment.payment_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_payment(self, payment_id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.payment WHERE payment_id = %s
            """, (payment_id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_payments(self, page: int = 1, page_size: int = 10) -> PaginateModel[Payment]:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.payment
                LIMIT %s OFFSET %s
            """, (page_size, (page - 1) * page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return PaginateModel[Payment](page=page, page_size=page_size, total=total, total_pages=total_pages, data=[Payment(**row) for row in rows])
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
