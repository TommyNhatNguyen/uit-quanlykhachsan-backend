import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.room_inventory_log import RoomInventoryLog, CreateRoomInventoryLog, UpdateRoomInventoryLog


class RoomInventoryLogRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_room_inventory_log(self, log: CreateRoomInventoryLog) -> RoomInventoryLog:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.room_inventory_log (id, room_id, room_number, room_type_id, is_available, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (log.id, log.room_id, log.room_number, log.room_type_id, log.is_available, log.created_at))
            conn.commit()
            return self.get_room_inventory_log(log.id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_room_inventory_log(self, id: int) -> RoomInventoryLog:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.room_inventory_log WHERE id = %s
            """, (id,))
            return RoomInventoryLog(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_room_inventory_log(self, log: UpdateRoomInventoryLog) -> RoomInventoryLog:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.room_inventory_log SET room_id = %s, room_number = %s, room_type_id = %s, is_available = %s, created_at = %s WHERE id = %s
            """, (log.room_id, log.room_number, log.room_type_id, log.is_available, log.created_at, log.id))
            conn.commit()
            return self.get_room_inventory_log(log.id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_room_inventory_log(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.room_inventory_log WHERE id = %s
            """, (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_room_inventory_logs(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.room_inventory_log
                ORDER BY id
                OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return {"page": page, "page_size": page_size, "total": total, "total_pages": total_pages, "data": [RoomInventoryLog(**row) for row in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
