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
                INSERT INTO dbo.booking (booking_id, customer_id, checkin_datetime, checkout_datetime, status, payment_id, hotel_id, created_at, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (booking.booking_id, booking.customer_id, booking.checkin_datetime, booking.checkout_datetime, booking.status, booking.payment_id, booking.hotel_id, booking.created_at, booking.notes))
            conn.commit()
            return self.get_booking(booking.booking_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_booking(self, booking_id: int) -> Booking:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.booking WHERE booking_id = %s
            """, (booking_id,))
            return Booking(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_booking(self, booking: UpdateBooking) -> Booking:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.booking SET customer_id = %s, checkin_datetime = %s, checkout_datetime = %s, status = %s, payment_id = %s, hotel_id = %s, created_at = %s, notes = %s WHERE booking_id = %s
            """, (booking.customer_id, booking.checkin_datetime, booking.checkout_datetime, booking.status, booking.payment_id, booking.hotel_id, booking.created_at, booking.notes, booking.booking_id))
            conn.commit()
            return self.get_booking(booking.booking_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_booking(self, booking_id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.booking WHERE booking_id = %s
            """, (booking_id,))
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
                SELECT * FROM dbo.booking
                ORDER BY booking_id
                OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return {"page": page, "page_size": page_size, "total": total, "total_pages": total_pages, "data": [Booking(**row) for row in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()