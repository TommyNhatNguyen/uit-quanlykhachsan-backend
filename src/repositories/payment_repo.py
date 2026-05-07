import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.payment import Payment, CreatePayment, UpdatePayment


class PaymentRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_payment(self, payment: CreatePayment) -> Payment:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.payment (cashier_id, total_payment, payment_method, booking_detail_id, created_at, is_deleted)
                OUTPUT INSERTED.id VALUES (%s, %s, %s, %s, %s, 0)
            """, (payment.cashier_id, payment.total_payment, payment.payment_method,
                  payment.booking_detail_id, payment.created_at))
            new_id = cur.fetchone()["id"]
            conn.commit()
            return self.get_payment(new_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_payment(self, id: int) -> Payment:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.payment WHERE id = %s", (id,))
            return Payment(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_payment(self, id: int, payment: Payment) -> Payment:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.payment SET cashier_id=%s, total_payment=%s, payment_method=%s,
                    booking_detail_id=%s, created_at=%s, is_deleted=%s WHERE id=%s
            """, (payment.cashier_id, payment.total_payment, payment.payment_method,
                  payment.booking_detail_id, payment.created_at, payment.is_deleted, id))
            conn.commit()
            return self.get_payment(id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_payment(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("UPDATE dbo.payment SET is_deleted=1 WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_payments(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.payment WHERE is_deleted=0
                ORDER BY id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            return {"page": page, "page_size": page_size, "total": total,
                    "total_pages": math.ceil(total / page_size) if total else 0,
                    "data": [Payment(**r) for r in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
