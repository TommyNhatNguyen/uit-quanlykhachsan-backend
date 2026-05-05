import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.room_inventory import RoomInventory, CreateRoomInventory, UpdateRoomInventory


class RoomInventoryRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_room_inventory(self, room_inventory: CreateRoomInventory) -> RoomInventory:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.room_inventory (room_id, room_number, room_type_id, is_available, updated_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (room_inventory.room_id, room_inventory.room_number, room_inventory.room_type_id, room_inventory.is_available, room_inventory.updated_at))
            conn.commit()
            return self.get_room_inventory(room_inventory.room_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_room_inventory(self, room_id: int) -> RoomInventory:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.room_inventory WHERE room_id = %s
            """, (room_id,))
            return RoomInventory(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_room_inventory(self, room_inventory: UpdateRoomInventory) -> RoomInventory:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.room_inventory SET room_number = %s, room_type_id = %s, is_available = %s, updated_at = %s WHERE room_id = %s
            """, (room_inventory.room_number, room_inventory.room_type_id, room_inventory.is_available, room_inventory.updated_at, room_inventory.room_id))
            conn.commit()
            return self.get_room_inventory(room_inventory.room_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_room_inventory(self, room_id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.room_inventory WHERE room_id = %s
            """, (room_id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_room_inventories(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.room_inventory
                ORDER BY room_id
                OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return {"page": page, "page_size": page_size, "total": total, "total_pages": total_pages, "data": [RoomInventory(**row) for row in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
