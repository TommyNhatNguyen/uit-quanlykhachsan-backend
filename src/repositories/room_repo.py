import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.room import Room, CreateRoom, UpdateRoom


class RoomRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_room(self, room: CreateRoom) -> Room:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.room (room_num, room_name, capacity, area, is_smoking, has_wifi, has_pool,
                    description, room_type_id, hotel_id, current_price_per_night, is_deleted, is_underconstruction)
                OUTPUT INSERTED.id
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0, %s)
            """, (room.room_num, room.room_name, room.capacity, room.area, room.is_smoking,
                  room.has_wifi, room.has_pool, room.description, room.room_type_id, room.hotel_id,
                  room.current_price_per_night, room.is_underconstruction))
            new_id = cur.fetchone()["id"]
            conn.commit()
            return self.get_room(new_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_room(self, id: int) -> Room:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.room WHERE id = %s", (id,))
            return Room(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_room(self, id: int, room: Room) -> Room:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.room SET room_num=%s, room_name=%s, capacity=%s, area=%s, is_smoking=%s,
                    has_wifi=%s, has_pool=%s, description=%s, room_type_id=%s, hotel_id=%s,
                    current_price_per_night=%s, is_deleted=%s, is_underconstruction=%s
                WHERE id=%s
            """, (room.room_num, room.room_name, room.capacity, room.area, room.is_smoking,
                  room.has_wifi, room.has_pool, room.description, room.room_type_id, room.hotel_id,
                  room.current_price_per_night, room.is_deleted, room.is_underconstruction, id))
            conn.commit()
            return self.get_room(id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_room(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("UPDATE dbo.room SET is_deleted=1 WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_rooms(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.room WHERE is_deleted=0
                ORDER BY id
                OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            return {"page": page, "page_size": page_size, "total": total,
                    "total_pages": math.ceil(total / page_size) if total else 0,
                    "data": [Room(**r) for r in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
