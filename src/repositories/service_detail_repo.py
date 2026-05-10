import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.service_detail import ServicesDetail, CreateServicesDetail, UpdateServicesDetail


class ServicesDetailRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_services_detail(self, detail: CreateServicesDetail) -> ServicesDetail:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.services_detail (booking_detail_id, service_id, quanity, price, total_amount)
                OUTPUT INSERTED.id VALUES (%s, %s, %s, %s, %s)
            """, (detail.booking_detail_id, detail.service_id, detail.quanity, detail.price, detail.total_amount))
            new_id = cur.fetchone()["id"]
            conn.commit()
            return self.get_services_detail(new_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_services_detail(self, id: int) -> ServicesDetail:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.services_detail WHERE id = %s", (id,))
            return ServicesDetail(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_services_detail(self, id: int, detail: ServicesDetail) -> ServicesDetail:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.services_detail SET booking_detail_id=%s, service_id=%s,
                    quanity=%s, price=%s, total_amount=%s WHERE id=%s
            """, (detail.booking_detail_id, detail.service_id, detail.quanity,
                  detail.price, detail.total_amount, id))
            conn.commit()
            return self.get_services_detail(id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_services_detail(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("DELETE FROM dbo.services_detail WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_services_details(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.services_detail
                ORDER BY id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            return {"page": page, "page_size": page_size, "total": total,
                    "total_pages": math.ceil(total / page_size) if total else 0,
                    "data": [ServicesDetail(**r) for r in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
