import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.service import Service, CreateService, UpdateService


class ServiceRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_service(self, service: CreateService) -> Service:
        conn = None

        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)

            cur.execute("""
                DECLARE @Inserted TABLE (
                    id INT
                );

                INSERT INTO dbo.service (
                    name,
                    catalog,
                    current_price
                )
                OUTPUT INSERTED.id INTO @Inserted
                VALUES (
                    %s, %s, %s
                );

                SELECT id FROM @Inserted;
            """, (
                service.name,
                service.catalog,
                service.current_price
            ))

            new_id = cur.fetchone()["id"]

            conn.commit()

            return self.get_service(new_id)

        except Exception as e:
            return JSONResponse(
                {"error": str(e)},
                status_code=500
            )

        finally:
            if conn:
                conn.close()

    def get_service(self, id: int) -> Service:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.service WHERE id = %s", (id,))
            return Service(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_service(self, id: int, service: Service) -> Service:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.service SET name=%s, catalog=%s, current_price=%s WHERE id=%s
            """, (service.name, service.catalog, service.current_price, id))
            conn.commit()
            return self.get_service(id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_service(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("DELETE FROM dbo.service WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_service_history_prices(self, service_id: int) -> list:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute(
                "SELECT * FROM dbo.service_price_log WHERE service_id = %s ORDER BY created_at DESC",
                (service_id,)
            )
            from src.models.service_price_log import ServicePriceLog
            return [ServicePriceLog(**r) for r in cur.fetchall()]
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_services(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.service
                ORDER BY id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            return {"page": page, "page_size": page_size, "total": total,
                    "total_pages": math.ceil(total / page_size) if total else 0,
                    "data": [Service(**r) for r in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
