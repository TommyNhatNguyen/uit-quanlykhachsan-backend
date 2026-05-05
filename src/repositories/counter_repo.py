import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.counter import Counter, CreateCounter, UpdateCounter


class CounterRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_counter(self, counter: CreateCounter) -> Counter:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.counters (name, value) VALUES (%s, %s)
            """, (counter.name, counter.value))
            conn.commit()
            return self.get_counter(counter.name)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_counter(self, name: str) -> Counter:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.counters WHERE name = %s
            """, (name,))
            return Counter(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_counter(self, counter: UpdateCounter) -> Counter:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.counters SET value = %s WHERE name = %s
            """, (counter.value, counter.name))
            conn.commit()
            return self.get_counter(counter.name)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_counter(self, name: str) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.counters WHERE name = %s
            """, (name,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_counters(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.counters
                ORDER BY name
                OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return {"page": page, "page_size": page_size, "total": total, "total_pages": total_pages, "data": [Counter(**row) for row in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
