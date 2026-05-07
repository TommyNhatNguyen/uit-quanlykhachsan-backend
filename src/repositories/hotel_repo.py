import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.hotel import Hotel, CreateHotel, UpdateHotel


class HotelRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_hotel(self, hotel: CreateHotel) -> Hotel:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.hotel (name, address, phone, is_deleted)
                OUTPUT INSERTED.id
                VALUES (%s, %s, %s, 0)
            """, (hotel.name, hotel.address, hotel.phone))
            new_id = cur.fetchone()["id"]
            conn.commit()
            return self.get_hotel(new_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_hotel(self, id: int) -> Hotel:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.hotel WHERE id = %s", (id,))
            return Hotel(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_hotel(self, id: int, hotel: Hotel) -> Hotel:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.hotel SET name=%s, address=%s, phone=%s, is_deleted=%s WHERE id=%s
            """, (hotel.name, hotel.address, hotel.phone, hotel.is_deleted, id))
            conn.commit()
            return self.get_hotel(id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_hotel(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("UPDATE dbo.hotel SET is_deleted=1 WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_hotels(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.hotel WHERE is_deleted=0
                ORDER BY id
                OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            return {"page": page, "page_size": page_size, "total": total,
                    "total_pages": math.ceil(total / page_size) if total else 0,
                    "data": [Hotel(**r) for r in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
