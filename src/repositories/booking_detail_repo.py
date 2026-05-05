import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.booking_detail import BookingDetail, CreateBookingDetail, UpdateBookingDetail
from src.models.paginate_model import PaginateModel


class BookingDetailRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_booking_detail(self, booking_detail: CreateBookingDetail) -> BookingDetail:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.booking_detail (booking_detail_id, booking_id, room_id, quantity, price, amount)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (booking_detail.booking_detail_id, booking_detail.booking_id, booking_detail.room_id, booking_detail.quantity, booking_detail.price, booking_detail.amount))
            conn.commit()
            return self.get_booking_detail(booking_detail.booking_detail_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_booking_detail(self, booking_detail_id: int) -> BookingDetail:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.booking_detail WHERE booking_detail_id = %s
            """, (booking_detail_id,))
            return BookingDetail(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_booking_detail(self, booking_detail: UpdateBookingDetail) -> BookingDetail:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.booking_detail SET booking_id = %s, room_id = %s, quantity = %s, price = %s, amount = %s WHERE booking_detail_id = %s
            """, (booking_detail.booking_id, booking_detail.room_id, booking_detail.quantity, booking_detail.price, booking_detail.amount, booking_detail.booking_detail_id))
            conn.commit()
            return self.get_booking_detail(booking_detail.booking_detail_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_booking_detail(self, booking_detail_id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.booking_detail WHERE booking_detail_id = %s
            """, (booking_detail_id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_booking_details(self, page: int = 1, page_size: int = 10) -> PaginateModel[BookingDetail]:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.booking_detail
                LIMIT %s OFFSET %s
            """, (page_size, (page - 1) * page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return PaginateModel[BookingDetail](page=page, page_size=page_size, total=total, total_pages=total_pages, data=[BookingDetail(**row) for row in rows])
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
