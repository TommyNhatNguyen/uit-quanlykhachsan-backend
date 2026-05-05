import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.payment_detail import PaymentDetail, CreatePaymentDetail, UpdatePaymentDetail


class PaymentDetailRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_payment_detail(self, payment_detail: CreatePaymentDetail) -> PaymentDetail:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.payment_detail (payment_detail_id, cashier_id, payment_id, total_payment, payment_method, payment_datetime)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (payment_detail.payment_detail_id, payment_detail.cashier_id, payment_detail.payment_id, payment_detail.total_payment, payment_detail.payment_method, payment_detail.payment_datetime))
            conn.commit()
            return self.get_payment_detail(payment_detail.payment_detail_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_payment_detail(self, payment_detail_id: int) -> PaymentDetail:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.payment_detail WHERE payment_detail_id = %s
            """, (payment_detail_id,))
            return PaymentDetail(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_payment_detail(self, payment_detail: UpdatePaymentDetail) -> PaymentDetail:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.payment_detail SET cashier_id = %s, payment_id = %s, total_payment = %s, payment_method = %s, payment_datetime = %s WHERE payment_detail_id = %s
            """, (payment_detail.cashier_id, payment_detail.payment_id, payment_detail.total_payment, payment_detail.payment_method, payment_detail.payment_datetime, payment_detail.payment_detail_id))
            conn.commit()
            return self.get_payment_detail(payment_detail.payment_detail_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_payment_detail(self, payment_detail_id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.payment_detail WHERE payment_detail_id = %s
            """, (payment_detail_id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_payment_details(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.payment_detail
                ORDER BY payment_detail_id
                OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return {"page": page, "page_size": page_size, "total": total, "total_pages": total_pages, "data": [PaymentDetail(**row) for row in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
