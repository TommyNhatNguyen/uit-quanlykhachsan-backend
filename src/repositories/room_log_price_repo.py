import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.room_log_price import RoomLogPrice, CreateRoomLogPrice, UpdateRoomLogPrice


class RoomLogPriceRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_room_log_price(self, log: CreateRoomLogPrice) -> RoomLogPrice:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.room_log_price (id, room_id, using_form_datetime, using_to_datetime, price_per_night)
                VALUES (%s, %s, %s, %s, %s)
            """, (log.id, log.room_id, log.using_form_datetime, log.using_to_datetime, log.price_per_night))
            conn.commit()
            return self.get_room_log_price(log.id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_room_log_price(self, id: int) -> RoomLogPrice:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.room_log_price WHERE id = %s
            """, (id,))
            return RoomLogPrice(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_room_log_price(self, log: UpdateRoomLogPrice) -> RoomLogPrice:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.room_log_price SET room_id = %s, using_form_datetime = %s, using_to_datetime = %s, price_per_night = %s WHERE id = %s
            """, (log.room_id, log.using_form_datetime, log.using_to_datetime, log.price_per_night, log.id))
            conn.commit()
            return self.get_room_log_price(log.id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_room_log_price(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.room_log_price WHERE id = %s
            """, (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_room_log_prices(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.room_log_price
                ORDER BY id
                OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return {"page": page, "page_size": page_size, "total": total, "total_pages": total_pages, "data": [RoomLogPrice(**row) for row in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
