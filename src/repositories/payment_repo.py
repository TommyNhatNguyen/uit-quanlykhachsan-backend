import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.payment import Payment, PopulatedPayment, CreatePayment, UpdatePayment, QueryPaymentsParams
from src.models.employee import Employee, PopulatedEmployee
from src.models.employee_account import EmployeeAccount
from src.models.booking_detail import BookingDetail

_JOIN = """
    FROM dbo.payment p
    LEFT JOIN dbo.employee e ON p.cashier_id = e.id
    LEFT JOIN dbo.employee_account ea ON e.employee_account_id = ea.id
    LEFT JOIN dbo.booking_detail bd ON p.booking_detail_id = bd.id
"""

_COLS = """
    p.id, p.cashier_id, p.total_payment, p.payment_method,
    p.booking_detail_id, p.created_at, p.is_deleted,
    e.id AS e_id, e.name AS e_name, e.birthday AS e_birthday, e.phone AS e_phone,
    e.is_working AS e_is_working, e.position AS e_position,
    e.start_working_date AS e_start_working_date,
    e.employee_account_id AS e_employee_account_id,
    e.is_deleted AS e_is_deleted, e.role AS e_role,
    ea.id AS ea_id, ea.username AS ea_username, ea.password AS ea_password,
    ea.created_at AS ea_created_at,
    bd.id AS bd_id, bd.booking_id AS bd_booking_id, bd.room_id AS bd_room_id,
    bd.checkin_date AS bd_checkin_date, bd.checkout_date AS bd_checkout_date,
    bd.quantity_of_nights AS bd_quantity_of_nights, bd.price_per_night AS bd_price_per_night,
    bd.total_room_amount AS bd_total_room_amount, bd.total_service_amount AS bd_total_service_amount,
    bd.total_amount AS bd_total_amount, bd.is_fully_paid AS bd_is_fully_paid, bd.status AS bd_status
"""


def _build_populated(row: dict) -> PopulatedPayment:
    account = EmployeeAccount(
        id=row["ea_id"], username=row["ea_username"], password=row["ea_password"],
        created_at=row["ea_created_at"]
    ) if row.get("ea_id") else None
    cashier = PopulatedEmployee(
        id=row["e_id"], name=row["e_name"], birthday=row["e_birthday"],
        phone=row["e_phone"], is_working=row["e_is_working"], position=row["e_position"],
        start_working_date=row["e_start_working_date"],
        employee_account_id=row["e_employee_account_id"],
        is_deleted=row["e_is_deleted"], role=row["e_role"],
        employee_account=account
    ) if row.get("e_id") else None
    booking_detail = BookingDetail(
        id=row["bd_id"], booking_id=row["bd_booking_id"], room_id=row["bd_room_id"],
        checkin_date=row["bd_checkin_date"], checkout_date=row["bd_checkout_date"],
        quantity_of_nights=row["bd_quantity_of_nights"], price_per_night=row["bd_price_per_night"],
        total_room_amount=row["bd_total_room_amount"], total_service_amount=row["bd_total_service_amount"],
        total_amount=row["bd_total_amount"], is_fully_paid=row["bd_is_fully_paid"], status=row["bd_status"]
    ) if row.get("bd_id") else None
    payment_data = {k: v for k, v in row.items()
                    if not k.startswith("e_") and not k.startswith("ea_") and not k.startswith("bd_")}
    return PopulatedPayment(**payment_data, cashier=cashier, booking_detail=booking_detail)


class PaymentRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_payment(self, payment: CreatePayment) -> PopulatedPayment:
        conn = None

        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)

            cur.execute("""
                DECLARE @Inserted TABLE (
                    id INT
                );

                INSERT INTO dbo.payment (
                    cashier_id,
                    total_payment,
                    payment_method,
                    booking_detail_id,
                    created_at,
                    is_deleted
                )
                OUTPUT INSERTED.id INTO @Inserted
                VALUES (
                    %s, %s, %s, %s, %s, 0
                );

                SELECT id FROM @Inserted;
            """, (
                payment.cashier_id,
                payment.total_payment,
                payment.payment_method,
                payment.booking_detail_id,
                payment.created_at
            ))

            new_id = cur.fetchone()["id"]

            conn.commit()

            return self.get_payment(new_id)

        except Exception as e:
            return JSONResponse(
                {"error": str(e)},
                status_code=500
            )

        finally:
            if conn:
                conn.close()

    def get_payment(self, id: int) -> PopulatedPayment:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute(f"SELECT {_COLS} {_JOIN} WHERE p.id = %s", (id,))
            row = cur.fetchone()
            if not row:
                return None
            return _build_populated(row)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_payment(self, id: int, payment: Payment) -> PopulatedPayment:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.payment SET cashier_id=%s, total_payment=%s, payment_method=%s,
                    booking_detail_id=%s, created_at=%s, is_deleted=%s WHERE id=%s
            """, (payment.cashier_id, payment.total_payment, payment.payment_method,
                  payment.booking_detail_id, payment.created_at, payment.is_deleted, id))
            conn.commit()
            return self.get_payment(id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_payment(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("UPDATE dbo.payment SET is_deleted=1 WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_payments(self, params: QueryPaymentsParams) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)

            where = "WHERE p.is_deleted=0"
            filter_args = []
            if params.booking_detail_id:
                where += " AND p.booking_detail_id = %s"
                filter_args.append(params.booking_detail_id)
            if params.cashier_id:
                where += " AND p.cashier_id = %s"
                filter_args.append(params.cashier_id)

            cur.execute(f"SELECT COUNT(*) AS total FROM dbo.payment p {where}", filter_args)
            total = cur.fetchone()["total"]

            cur.execute(
                f"SELECT {_COLS} {_JOIN} {where} ORDER BY p.id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY",
                filter_args + [(params.page - 1) * params.page_size, params.page_size]
            )
            rows = cur.fetchall()

            return {
                "page": params.page, "page_size": params.page_size, "total": total,
                "total_pages": math.ceil(total / params.page_size) if total else 0,
                "data": [_build_populated(r) for r in rows]
            }
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
