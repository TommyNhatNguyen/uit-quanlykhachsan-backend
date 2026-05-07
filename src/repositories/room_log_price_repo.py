import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.room_price_log import RoomPriceLog, CreateRoomPriceLog, UpdateRoomPriceLog


class RoomPriceLogRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_room_price_log(self, log: CreateRoomPriceLog) -> RoomPriceLog:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.room_price_log (room_id, created_at, price_per_night)
                OUTPUT INSERTED.id VALUES (%s, %s, %s)
            """, (log.room_id, log.created_at, log.price_per_night))
            new_id = cur.fetchone()["id"]
            conn.commit()
            return self.get_room_price_log(new_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_room_price_log(self, id: int) -> RoomPriceLog:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.room_price_log WHERE id = %s", (id,))
            return RoomPriceLog(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_room_price_log(self, id: int, log: RoomPriceLog) -> RoomPriceLog:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.room_price_log SET room_id=%s, created_at=%s, price_per_night=%s WHERE id=%s
            """, (log.room_id, log.created_at, log.price_per_night, id))
            conn.commit()
            return self.get_room_price_log(id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_room_price_log(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("DELETE FROM dbo.room_price_log WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_room_price_logs(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.room_price_log
                ORDER BY id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            return {"page": page, "page_size": page_size, "total": total,
                    "total_pages": math.ceil(total / page_size) if total else 0,
                    "data": [RoomPriceLog(**r) for r in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
