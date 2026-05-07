import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.service import ServiceItem, CreateServiceItem, UpdateServiceItem


class ServiceItemRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_service_item(self, service_item: CreateServiceItem) -> ServiceItem:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.service_item (service_item_id, service_item_name, catalog, price, used_count)
                VALUES (%s, %s, %s, %s, %s)
            """, (service_item.service_item_id, service_item.service_item_name, service_item.catalog, service_item.price, service_item.used_count))
            conn.commit()
            return self.get_service_item(service_item.service_item_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_service_item(self, service_item_id: int) -> ServiceItem:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.service_item WHERE service_item_id = %s
            """, (service_item_id,))
            return ServiceItem(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_service_item(self, service_item: UpdateServiceItem) -> ServiceItem:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.service_item SET service_item_name = %s, catalog = %s, price = %s, used_count = %s WHERE service_item_id = %s
            """, (service_item.service_item_name, service_item.catalog, service_item.price, service_item.used_count, service_item.service_item_id))
            conn.commit()
            return self.get_service_item(service_item.service_item_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_service_item(self, service_item_id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.service_item WHERE service_item_id = %s
            """, (service_item_id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_service_items(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.service_item
                ORDER BY service_item_id
                OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return {"page": page, "page_size": page_size, "total": total, "total_pages": total_pages, "data": [ServiceItem(**row) for row in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
