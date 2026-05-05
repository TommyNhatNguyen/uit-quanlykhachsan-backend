import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.room_type import RoomType, CreateRoomType, UpdateRoomType
from src.models.paginate_model import PaginateModel


class RoomTypeRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_room_type(self, room_type: CreateRoomType) -> RoomType:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.room_type (room_type_id, room_type_name) VALUES (%s, %s)
            """, (room_type.room_type_id, room_type.room_type_name))
            conn.commit()
            return self.get_room_type(room_type.room_type_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_room_type(self, room_type_id: int) -> RoomType:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.room_type WHERE room_type_id = %s
            """, (room_type_id,))
            return RoomType(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_room_type(self, room_type: UpdateRoomType) -> RoomType:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.room_type SET room_type_name = %s WHERE room_type_id = %s
            """, (room_type.room_type_name, room_type.room_type_id))
            conn.commit()
            return self.get_room_type(room_type.room_type_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_room_type(self, room_type_id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.room_type WHERE room_type_id = %s
            """, (room_type_id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_room_types(self, page: int = 1, page_size: int = 10) -> PaginateModel[RoomType]:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.room_type
                LIMIT %s OFFSET %s
            """, (page_size, (page - 1) * page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return PaginateModel[RoomType](page=page, page_size=page_size, total=total, total_pages=total_pages, data=[RoomType(**row) for row in rows])
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
