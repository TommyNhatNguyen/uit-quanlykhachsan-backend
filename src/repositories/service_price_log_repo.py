import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.service_price_log import (
    ServicePriceLog, PopulatedServicePriceLog,
    CreateServicePriceLog, UpdateServicePriceLog, QueryServicePriceLogsParams
)
from src.models.service import Service

_JOIN = """
    FROM dbo.service_price_log spl
    LEFT JOIN dbo.service s ON spl.service_id = s.id
"""

_COLS = """
    spl.id, spl.service_id, spl.created_at, spl.price,
    s.id AS s_id, s.name AS s_name, s.catalog AS s_catalog, s.current_price AS s_current_price
"""


def _build_populated(row: dict) -> PopulatedServicePriceLog:
    service = Service(
        id=row["s_id"], name=row["s_name"],
        catalog=row["s_catalog"], current_price=row["s_current_price"]
    ) if row.get("s_id") else None
    log_data = {k: v for k, v in row.items() if not k.startswith("s_")}
    return PopulatedServicePriceLog(**log_data, service=service)


class ServicePriceLogRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_service_price_log(self, log: CreateServicePriceLog) -> PopulatedServicePriceLog:
        conn = None
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DECLARE @Inserted TABLE (id INT);
                INSERT INTO dbo.service_price_log (service_id, created_at, price)
                OUTPUT INSERTED.id INTO @Inserted
                VALUES (%s, %s, %s);
                SELECT id FROM @Inserted;
            """, (log.service_id, log.created_at, log.price))
            new_id = cur.fetchone()["id"]
            conn.commit()
            return self.get_service_price_log(new_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            if conn:
                conn.close()

    def get_service_price_log(self, id: int) -> PopulatedServicePriceLog:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute(f"SELECT {_COLS} {_JOIN} WHERE spl.id = %s", (id,))
            row = cur.fetchone()
            if not row:
                return None
            return _build_populated(row)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_service_price_log(self, id: int, log: ServicePriceLog) -> PopulatedServicePriceLog:
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

    def get_list_service_price_logs(self, params: QueryServicePriceLogsParams) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)

            where = "WHERE 1=1"
            filter_args = []
            if params.service_id:
                where += " AND spl.service_id = %s"
                filter_args.append(params.service_id)

            cur.execute(f"SELECT COUNT(*) AS total FROM dbo.service_price_log spl {where}", filter_args)
            total = cur.fetchone()["total"]

            cur.execute(
                f"SELECT {_COLS} {_JOIN} {where} ORDER BY spl.id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY",
                filter_args + [(params.page - 1) * params.page_size, params.page_size]
            )
            rows = cur.fetchall()

            return {
                "page": params.page, "page_size": params.page_size, "total": total,
                "total_pages": math.ceil(total / params.page_size) if total else 0,
                "data": [_build_populated(r) for r in rows]
            }
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
