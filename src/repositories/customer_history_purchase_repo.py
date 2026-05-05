import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.customer_history_purchase import CustomerHistoryPurchase, CreateCustomerHistoryPurchase, UpdateCustomerHistoryPurchase
from src.models.paginate_model import PaginateModel


class CustomerHistoryPurchaseRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_customer_history_purchase(self, chp: CreateCustomerHistoryPurchase) -> CustomerHistoryPurchase:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.customer_history_purchase (id, customer_id, booking_id, booking_paid, cumulative_paid)
                VALUES (%s, %s, %s, %s, %s)
            """, (chp.id, chp.customer_id, chp.booking_id, chp.booking_paid, chp.cumulative_paid))
            conn.commit()
            return self.get_customer_history_purchase(chp.id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_customer_history_purchase(self, id: int) -> CustomerHistoryPurchase:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.customer_history_purchase WHERE id = %s
            """, (id,))
            return CustomerHistoryPurchase(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_customer_history_purchase(self, chp: UpdateCustomerHistoryPurchase) -> CustomerHistoryPurchase:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.customer_history_purchase SET customer_id = %s, booking_id = %s, booking_paid = %s, cumulative_paid = %s WHERE id = %s
            """, (chp.customer_id, chp.booking_id, chp.booking_paid, chp.cumulative_paid, chp.id))
            conn.commit()
            return self.get_customer_history_purchase(chp.id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_customer_history_purchase(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.customer_history_purchase WHERE id = %s
            """, (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_customer_history_purchases(self, page: int = 1, page_size: int = 10) -> PaginateModel[CustomerHistoryPurchase]:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.customer_history_purchase
                LIMIT %s OFFSET %s
            """, (page_size, (page - 1) * page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return PaginateModel[CustomerHistoryPurchase](page=page, page_size=page_size, total=total, total_pages=total_pages, data=[CustomerHistoryPurchase(**row) for row in rows])
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
