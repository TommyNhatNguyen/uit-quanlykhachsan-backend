import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.booking import Booking, PopulatedBooking, CreateBooking, UpdateBooking, QueryBookingsParams
from src.models.customer import PopulatedCustomer
from src.models.membership import Membership
from src.models.booking_detail import PopulatedBookingDetail


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

    def get_booking(self, id: int) -> PopulatedBooking:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT
                    b.id, b.customer_id, b.created_at, b.notes, b.is_fully_paid, b.is_deleted,
                    c.id AS c_id, c.name AS c_name, c.phone AS c_phone, c.sex AS c_sex,
                    c.identification_id AS c_identification_id, c.email AS c_email,
                    c.birthday AS c_birthday, c.membership_type_id AS c_membership_type_id,
                    m.id AS m_id, m.name AS m_name, m.paid_from AS m_paid_from,
                    m.paid_to AS m_paid_to, m.is_deleted AS m_is_deleted
                FROM dbo.booking b
                LEFT JOIN dbo.customer c ON b.customer_id = c.id
                LEFT JOIN dbo.membership m ON c.membership_type_id = m.id
                WHERE b.id = %s
            """, (id,))
            row = cur.fetchone()
            if not row:
                return None
            cur.execute("SELECT * FROM dbo.booking_detail WHERE booking_id = %s", (id,))
            details = [PopulatedBookingDetail(**d) for d in cur.fetchall()]
            membership = Membership(
                id=row["m_id"], name=row["m_name"], paid_from=row["m_paid_from"],
                paid_to=row["m_paid_to"], is_deleted=row["m_is_deleted"]
            ) if row.get("m_id") else None
            customer = PopulatedCustomer(
                id=row["c_id"], name=row["c_name"], phone=row["c_phone"],
                sex=row["c_sex"], identification_id=row["c_identification_id"],
                email=row["c_email"], birthday=row["c_birthday"],
                membership_type_id=row["c_membership_type_id"],
                membership_type=membership
            ) if row.get("c_id") else None
            booking_data = {k: v for k, v in row.items() if not k.startswith("c_") and not k.startswith("m_")}
            return PopulatedBooking(**booking_data, customer=customer, booking_details=details or None)
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

    def get_list_bookings(self, params: QueryBookingsParams) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)

            where = "WHERE b.is_deleted=0"
            filter_args = []
            if params.customer_id:
                where += " AND b.customer_id = %s"
                filter_args.append(params.customer_id)
            if params.is_fully_paid is not None:
                where += " AND b.is_fully_paid = %s"
                filter_args.append(params.is_fully_paid)

            cur.execute(f"SELECT COUNT(*) AS total FROM dbo.booking b {where}", filter_args)
            total = cur.fetchone()["total"]

            cur.execute(f"""
                SELECT
                    b.id, b.customer_id, b.created_at, b.notes, b.is_fully_paid, b.is_deleted,
                    c.id AS c_id, c.name AS c_name, c.phone AS c_phone, c.sex AS c_sex,
                    c.identification_id AS c_identification_id, c.email AS c_email,
                    c.birthday AS c_birthday, c.membership_type_id AS c_membership_type_id,
                    m.id AS m_id, m.name AS m_name, m.paid_from AS m_paid_from,
                    m.paid_to AS m_paid_to, m.is_deleted AS m_is_deleted
                FROM dbo.booking b
                LEFT JOIN dbo.customer c ON b.customer_id = c.id
                LEFT JOIN dbo.membership m ON c.membership_type_id = m.id
                {where} ORDER BY b.id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, filter_args + [(params.page - 1) * params.page_size, params.page_size])
            rows = cur.fetchall()

            booking_ids = [row["id"] for row in rows]
            details_by_booking = {}
            if booking_ids:
                placeholders = ",".join(["%s"] * len(booking_ids))
                cur.execute(
                    f"SELECT * FROM dbo.booking_detail WHERE booking_id IN ({placeholders})",
                    booking_ids
                )
                for d in cur.fetchall():
                    details_by_booking.setdefault(d["booking_id"], []).append(PopulatedBookingDetail(**d))

            data = []
            for row in rows:
                membership = Membership(
                    id=row["m_id"], name=row["m_name"], paid_from=row["m_paid_from"],
                    paid_to=row["m_paid_to"], is_deleted=row["m_is_deleted"]
                ) if row.get("m_id") else None
                customer = PopulatedCustomer(
                    id=row["c_id"], name=row["c_name"], phone=row["c_phone"],
                    sex=row["c_sex"], identification_id=row["c_identification_id"],
                    email=row["c_email"], birthday=row["c_birthday"],
                    membership_type_id=row["c_membership_type_id"],
                    membership_type=membership
                ) if row.get("c_id") else None
                booking_data = {k: v for k, v in row.items() if not k.startswith("c_") and not k.startswith("m_")}
                data.append(PopulatedBooking(
                    **booking_data,
                    customer=customer,
                    booking_details=details_by_booking.get(row["id"])
                ))

            return {
                "page": params.page, "page_size": params.page_size, "total": total,
                "total_pages": math.ceil(total / params.page_size) if total else 0,
                "data": data
            }
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
