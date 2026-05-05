import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.room import Room, CreateRoom, UpdateRoom
from src.models.paginate_model import PaginateModel


class RoomRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_room(self, room: CreateRoom) -> Room:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.room (room_id, room_number, room_type_id, price_per_night, capacity, room_area, is_smoking, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (room.room_id, room.room_number, room.room_type_id, room.price_per_night, room.capacity, room.room_area, room.is_smoking, room.description))
            conn.commit()
            return self.get_room(room.room_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_room(self, room_id: int) -> Room:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.room WHERE room_id = %s
            """, (room_id,))
            return Room(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_room(self, room: UpdateRoom) -> Room:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.room SET room_number = %s, room_type_id = %s, price_per_night = %s, capacity = %s, room_area = %s, is_smoking = %s, description = %s WHERE room_id = %s
            """, (room.room_number, room.room_type_id, room.price_per_night, room.capacity, room.room_area, room.is_smoking, room.description, room.room_id))
            conn.commit()
            return self.get_room(room.room_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_room(self, room_id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.room WHERE room_id = %s
            """, (room_id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_rooms(self, page: int = 1, page_size: int = 10) -> PaginateModel[Room]:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.room
                LIMIT %s OFFSET %s
            """, (page_size, (page - 1) * page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return PaginateModel[Room](page=page, page_size=page_size, total=total, total_pages=total_pages, data=[Room(**row) for row in rows])
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
