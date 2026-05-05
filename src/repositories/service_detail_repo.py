import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.service_detail import ServiceDetail, CreateServiceDetail, UpdateServiceDetail


class ServiceDetailRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_service_detail(self, service_detail: CreateServiceDetail) -> ServiceDetail:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.service_detail (service_detail, booking_id, service_item_id, quantity, price, amount)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (service_detail.service_detail, service_detail.booking_id, service_detail.service_item_id, service_detail.quantity, service_detail.price, service_detail.amount))
            conn.commit()
            return self.get_service_detail(service_detail.service_detail)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_service_detail(self, service_detail_id: int) -> ServiceDetail:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.service_detail WHERE service_detail = %s
            """, (service_detail_id,))
            return ServiceDetail(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_service_detail(self, service_detail: UpdateServiceDetail) -> ServiceDetail:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.service_detail SET booking_id = %s, service_item_id = %s, quantity = %s, price = %s, amount = %s WHERE service_detail = %s
            """, (service_detail.booking_id, service_detail.service_item_id, service_detail.quantity, service_detail.price, service_detail.amount, service_detail.service_detail))
            conn.commit()
            return self.get_service_detail(service_detail.service_detail)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_service_detail(self, service_detail_id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.service_detail WHERE service_detail = %s
            """, (service_detail_id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_service_details(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.service_detail
                ORDER BY service_detail
                OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return {"page": page, "page_size": page_size, "total": total, "total_pages": total_pages, "data": [ServiceDetail(**row) for row in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
