import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.service_price_log import ServicePriceLog, CreateServicePriceLog, UpdateServicePriceLog


class ServicePriceLogRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_service_price_log(self, log: CreateServicePriceLog) -> ServicePriceLog:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.service_price_log (service_id, created_at, price)
                OUTPUT INSERTED.id VALUES (%s, %s, %s)
            """, (log.service_id, log.created_at, log.price))
            new_id = cur.fetchone()["id"]
            conn.commit()
            return self.get_service_price_log(new_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_service_price_log(self, id: int) -> ServicePriceLog:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.service_price_log WHERE id = %s", (id,))
            return ServicePriceLog(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_service_price_log(self, id: int, log: ServicePriceLog) -> ServicePriceLog:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.service_price_log SET service_id=%s, created_at=%s, price=%s WHERE id=%s
            """, (log.service_id, log.created_at, log.price, id))
            conn.commit()
            return self.get_service_price_log(id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_service_price_log(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("DELETE FROM dbo.service_price_log WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_service_price_logs(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.service_price_log
                ORDER BY id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            return {"page": page, "page_size": page_size, "total": total,
                    "total_pages": math.ceil(total / page_size) if total else 0,
                    "data": [ServicePriceLog(**r) for r in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
