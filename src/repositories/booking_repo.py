import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.booking import Booking, CreateBooking, UpdateBooking


class BookingRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_booking(self, booking: CreateBooking) -> Booking:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.booking (customer_id, created_at, notes, is_fully_paid, is_deleted)
                OUTPUT INSERTED.id VALUES (%s, %s, %s, %s, 0)
            """, (booking.customer_id, booking.created_at, booking.notes, booking.is_fully_paid))
            new_id = cur.fetchone()["id"]
            conn.commit()
            return self.get_booking(new_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_booking(self, id: int) -> Booking:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.booking WHERE id = %s", (id,))
            return Booking(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_booking(self, id: int, booking: Booking) -> Booking:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.booking SET customer_id=%s, created_at=%s, notes=%s,
                    is_fully_paid=%s, is_deleted=%s WHERE id=%s
            """, (booking.customer_id, booking.created_at, booking.notes,
                  booking.is_fully_paid, booking.is_deleted, id))
            conn.commit()
            return self.get_booking(id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_booking(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("UPDATE dbo.booking SET is_deleted=1 WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_bookings(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.booking WHERE is_deleted=0
                ORDER BY id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            return {"page": page, "page_size": page_size, "total": total,
                    "total_pages": math.ceil(total / page_size) if total else 0,
                    "data": [Booking(**r) for r in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
