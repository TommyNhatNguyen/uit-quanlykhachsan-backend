import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.booking_detail import BookingDetail, BookingStatus, CreateBookingDetail, UpdateBookingDetail


class BookingDetailRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_booking_detail(self, detail: CreateBookingDetail) -> BookingDetail:
        conn = None

        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)

            cur.execute("""
                DECLARE @Inserted TABLE (
                    id INT
                );

                INSERT INTO dbo.booking_detail (
                    customer_id,
                    booking_id,
                    room_id,
                    checkin_date,
                    checkout_date,
                    quantity_of_nights,
                    price_per_night,
                    total_room_amount,
                    total_service_amount,
                    total_amount,
                    is_fully_paid,
                    status
                )
                OUTPUT INSERTED.id INTO @Inserted
                VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, 0, %s
                );

                SELECT id FROM @Inserted;
            """, (
                detail.customer_id,
                detail.booking_id,
                detail.room_id,
                detail.checkin_date,
                detail.checkout_date,
                detail.quantity_of_nights,
                detail.price_per_night,
                detail.total_room_amount,
                detail.total_service_amount,
                detail.total_amount,
                detail.status
            ))

            new_id = cur.fetchone()["id"]

            conn.commit()

            return self.get_booking_detail(new_id)

        except Exception as e:
            return JSONResponse(
                {"error": str(e)},
                status_code=500
            )

        finally:
            if conn:
                conn.close()

    def get_booking_detail(self, id: int) -> BookingDetail:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.booking_detail WHERE id = %s", (id,))
            return BookingDetail(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_booking_detail(self, id: int, detail: BookingDetail) -> BookingDetail:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.booking_detail SET booking_id=%s, room_id=%s, checkin_date=%s,
                    checkout_date=%s, quantity_of_nights=%s, price_per_night=%s,
                    total_room_amount=%s, total_service_amount=%s, total_amount=%s,
                    is_fully_paid=%s, status=%s WHERE id=%s
            """, (detail.booking_id, detail.room_id, detail.checkin_date, detail.checkout_date,
                  detail.quantity_of_nights, detail.price_per_night, detail.total_room_amount,
                  detail.total_service_amount, detail.total_amount, detail.is_fully_paid,
                  detail.status, id))
            conn.commit()
            return self.get_booking_detail(id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_booking_detail(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("DELETE FROM dbo.booking_detail WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_booking_details(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.booking_detail
                ORDER BY id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            return {"page": page, "page_size": page_size, "total": total,
                    "total_pages": math.ceil(total / page_size) if total else 0,
                    "data": [BookingDetail(**r) for r in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
