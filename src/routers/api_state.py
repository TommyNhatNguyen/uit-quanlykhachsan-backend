from datetime import date
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

import src.helpers as helpers
import src.constants as constants
from src.db.db import db
from src.db.utils import DELETE_ORDER, ensure_extras, ensure_reference_data

router = APIRouter()


# ── GET /api/state ────────────────────────────────────────────────────────────

@router.get("/api/state")
def get_state():
    conn = db.get_connection()
    try:
        cur = conn.cursor(as_dict=True)
        ensure_extras(cur)
        ensure_reference_data(cur)
        conn.commit()

        cur.execute("""
            SELECT
                b.booking_id,
                c.customer_id,
                c.customer_name,
                CAST(b.checkin_datetime  AS DATE) AS checkin,
                CAST(b.checkout_datetime AS DATE) AS checkout,
                b.status,
                COALESCE(p.status, 'unpaid')      AS payment_status,
                COALESCE(SUM(bd.amount), 0)       AS total_amount,
                COALESCE(
                    STRING_AGG(r.room_number, ', ') WITHIN GROUP (ORDER BY r.room_number),
                    ''
                )                                  AS rooms,
                COALESCE(b.notes, '')             AS notes
            FROM dbo.booking b
            JOIN dbo.customer c             ON c.customer_id  = b.customer_id
            LEFT JOIN dbo.payment p         ON p.payment_id   = b.payment_id
            LEFT JOIN dbo.booking_detail bd ON bd.booking_id  = b.booking_id
            LEFT JOIN dbo.room r            ON r.room_id      = bd.room_id
            GROUP BY b.booking_id, c.customer_id, c.customer_name,
                     b.checkin_datetime, b.checkout_datetime, b.status,
                     p.status, b.notes
            ORDER BY b.booking_id DESC
        """)
        bookings = [
            {
                "id":         helpers.int_to_bk(r["booking_id"]),
                "customerId": r["customer_id"],
                "customer":   r["customer_name"],
                "checkin":    helpers.val(r["checkin"])  or "",
                "checkout":   helpers.val(r["checkout"]) or "",
                "rooms":      r["rooms"] or "",
                "status":     (r["status"] or "pending").lower(),
                "payment":    (r["payment_status"] or "unpaid").lower(),
                "amount":     float(r["total_amount"] or 0),
                "notes":      r["notes"] or "",
            }
            for r in cur.fetchall()
        ]

        cur.execute("""
            SELECT
                c.customer_id,
                c.customer_name,
                c.sex,
                c.phone,
                c.email,
                c.birthday,
                mt.membership_type_name AS tier,
                c.total_paid
            FROM dbo.customer c
            LEFT JOIN dbo.membership_type mt ON mt.membership_type_id = c.membership_type_id
            ORDER BY c.customer_id
        """)
        customers = [
            {
                "id":        r["customer_id"],
                "name":      r["customer_name"],
                "sex":       r["sex"] or "Nam",
                "phone":     r["phone"] or "",
                "email":     r["email"] or "",
                "dob":       helpers.val(r["birthday"]) or "",
                "tier":      r["tier"] or "Silver",
                "totalPaid": float(r["total_paid"] or 0),
                "notes":     "",
            }
            for r in cur.fetchall()
        ]

        cur.execute("""
            SELECT
                r.room_number,
                rt.room_type_name       AS type,
                r.price_per_night,
                r.capacity,
                r.room_area,
                r.is_smoking,
                ri.is_available
            FROM dbo.room r
            JOIN dbo.room_type rt           ON rt.room_type_id = r.room_type_id
            LEFT JOIN dbo.room_inventory ri ON ri.room_id      = r.room_id
            ORDER BY r.room_number
        """)
        rooms = [
            {
                "number":   r["room_number"],
                "type":     r["type"],
                "capacity": r["capacity"] or "2 khách",
                "area":     r["room_area"] or "—",
                "price":    float(r["price_per_night"] or 0),
                "smoking":  bool(r["is_smoking"]),
                "status":   helpers.is_avail_to_status(r["is_available"]),
            }
            for r in cur.fetchall()
        ]

        cur.execute("""
            SELECT service_item_id, service_item_name, catalog, price, used_count
            FROM dbo.service_item
            ORDER BY service_item_id
        """)
        services = [
            {
                "id":      r["service_item_id"],
                "name":    r["service_item_name"],
                "catalog": r["catalog"],
                "price":   float(r["price"] or 0),
                "used":    int(r["used_count"] or 0),
            }
            for r in cur.fetchall()
        ]

        cur.execute("""
            SELECT employee_id, employee_name, birthday, phone,
                   is_working, position, start_working_date
            FROM dbo.employee
            ORDER BY employee_id
        """)
        employees = [
            {
                "id":       helpers.int_to_emp(r["employee_id"]),
                "name":     r["employee_name"],
                "dob":      helpers.val(r["birthday"]) or "",
                "phone":    r["phone"] or "",
                "position": r["position"] or "",
                "start":    helpers.val(r["start_working_date"]) or "",
                "working":  str(r["is_working"]).lower() == "true",
            }
            for r in cur.fetchall()
        ]

        cur.execute("""
            SELECT
                pd.payment_detail_id,
                b.booking_id,
                c.customer_name,
                pd.payment_method,
                e.employee_name   AS cashier,
                pd.payment_datetime,
                pd.total_payment,
                p.status
            FROM dbo.payment_detail pd
            JOIN dbo.payment  p  ON p.payment_id   = pd.payment_id
            JOIN dbo.booking  b  ON b.payment_id   = p.payment_id
            JOIN dbo.customer c  ON c.customer_id  = b.customer_id
            LEFT JOIN dbo.employee e ON e.employee_id = pd.cashier_id
            ORDER BY pd.payment_detail_id DESC
        """)
        payments = [
            {
                "id":        helpers.int_to_pay(r["payment_detail_id"]),
                "bookingId": helpers.int_to_bk(r["booking_id"]),
                "customer":  r["customer_name"],
                "method":    r["payment_method"] or "",
                "cashier":   r["cashier"] or "",
                "datetime":  helpers.val(r["payment_datetime"]) or "",
                "amount":    float(r["total_payment"] or 0),
                "status":    (r["status"] or "success").lower(),
            }
            for r in cur.fetchall()
        ]

        cur.execute("""
            SELECT rlp.id, r.room_number,
                   rlp.using_form_datetime, rlp.using_to_datetime,
                   rlp.price_per_night
            FROM dbo.room_log_price rlp
            JOIN dbo.room r ON r.room_id = rlp.room_id
            ORDER BY rlp.id
        """)
        price_logs = [
            {
                "id":         r["id"],
                "roomNumber": r["room_number"],
                "from":       helpers.val(r["using_form_datetime"]) or "",
                "to":         helpers.val(r["using_to_datetime"]),
                "price":      float(r["price_per_night"] or 0),
            }
            for r in cur.fetchall()
        ]

        cur.execute("SELECT * FROM dbo.notifications ORDER BY id DESC")
        notifications = [
            {
                "id":     r["id"],
                "title":  r["title"],
                "sub":    r["sub"] or "",
                "time":   r["time_str"] or "",
                "unread": bool(r["unread"]),
                "icon":   r["icon"] or "🔔",
            }
            for r in cur.fetchall()
        ]

        cur.execute("SELECT * FROM dbo.counters")
        counters = {r["name"]: r["value"] for r in cur.fetchall()}

        cur.close()
        return {
            "bookings":      bookings,
            "customers":     customers,
            "rooms":         rooms,
            "services":      services,
            "employees":     employees,
            "payments":      payments,
            "priceLogs":     price_logs,
            "notifications": notifications,
            "counters":      counters,
        }
    except Exception as e:
        import traceback; traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        conn.close()


# ── PUT /api/state ────────────────────────────────────────────────────────────

@router.put("/api/state")
async def save_state(request: Request):
    data = await request.json()
    if not data:
        return JSONResponse({"error": "No JSON body"}, status_code=400)

    conn = db.get_connection()
    try:
        cur = conn.cursor(as_dict=True)
        ensure_extras(cur)

        for tbl in DELETE_ORDER:
            cur.execute(f"DELETE FROM {tbl}")

        cur.execute("INSERT INTO dbo.membership_type VALUES (1, N'Silver', 0, 20000000)")
        cur.execute("INSERT INTO dbo.membership_type VALUES (2, N'Gold', 20000000, 50000000)")
        cur.execute("INSERT INTO dbo.membership_type VALUES (3, N'Diamond', 50000000, NULL)")
        cur.execute("INSERT INTO dbo.room_type VALUES (1, N'Standard')")
        cur.execute("INSERT INTO dbo.room_type VALUES (2, N'Deluxe')")
        cur.execute("INSERT INTO dbo.room_type VALUES (3, N'Suite')")
        cur.execute("INSERT INTO dbo.room_type VALUES (4, N'Family')")

        for c in data.get("customers", []):
            cur.execute(
                """INSERT INTO dbo.customer
                       (customer_id, customer_name, sex, phone, email, birthday,
                        membership_type_id, total_paid)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (c["id"], c["name"], c.get("sex", ""), c.get("phone", ""),
                 c.get("email", ""), c.get("dob") or None,
                 constants.TIER_ID.get(c.get("tier", "Silver"), 1), c.get("totalPaid", 0)),
            )

        emp_name_to_id: dict = {}
        for e in data.get("employees", []):
            eid = helpers.emp_to_int(e["id"])
            emp_name_to_id[e["name"]] = eid
            cur.execute(
                """INSERT INTO dbo.employee
                       (employee_id, employee_name, birthday, phone,
                        is_working, position, start_working_date)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (eid, e["name"], e.get("dob") or None, e.get("phone", ""),
                 str(e.get("working", True)).lower(),
                 e.get("position", ""), e.get("start") or None),
            )

        for s in data.get("services", []):
            cur.execute(
                """INSERT INTO dbo.service_item
                       (service_item_id, service_item_name, catalog, price, used_count)
                   VALUES (%s, %s, %s, %s, %s)""",
                (s["id"], s["name"], s["catalog"], s["price"], s.get("used", 0)),
            )

        rnum_id_map: dict = {}
        for r in data.get("rooms", []):
            rid     = helpers.rnum_to_id(r["number"])
            rnum_id_map[r["number"]] = rid
            type_id = constants.RTYPE_ID.get(r["type"], 1)
            is_av   = constants.IS_AVAIL.get(r.get("status", "available"), 1.0)

            cur.execute(
                """INSERT INTO dbo.room_inventory
                       (room_id, room_number, room_type_id, is_available, updated_at)
                   VALUES (%s, %s, %s, %s, GETDATE())""",
                (rid, r["number"], type_id, is_av),
            )
            cur.execute(
                """INSERT INTO dbo.room
                       (room_id, room_number, room_type_id, price_per_night,
                        capacity, room_area, is_smoking, description)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (rid, r["number"], type_id, r["price"],
                 r.get("capacity", "2 khách"), r.get("area", "—"),
                 1 if r.get("smoking") else 0, ""),
            )

        room_map = {r["number"]: r for r in data.get("rooms", [])}

        for b in data.get("bookings", []):
            bid    = helpers.bk_to_int(b["id"])
            p_stat = b.get("payment", "unpaid")

            cur.execute(
                "INSERT INTO dbo.payment (payment_id, status) VALUES (%s, %s)",
                (bid, p_stat),
            )
            cur.execute(
                """INSERT INTO dbo.booking
                       (booking_id, customer_id, checkin_datetime, checkout_datetime,
                        status, payment_id, hotel_id, created_at, notes)
                   VALUES (%s, %s, %s, %s, %s, %s, 1, GETDATE(), %s)""",
                (bid, b.get("customerId"),
                 b.get("checkin"), b.get("checkout"),
                 b.get("status", "pending").lower(),
                 bid, b.get("notes", "")),
            )

            rooms_str = b.get("rooms", "")
            rnums = [n.strip() for n in rooms_str.split(",") if n.strip()]
            try:
                nights = max(1, (
                    date.fromisoformat(b["checkout"]) -
                    date.fromisoformat(b["checkin"])
                ).days) if (rnums and b.get("checkin") and b.get("checkout")) else 1
            except Exception:
                nights = 1

            for idx, rnum in enumerate(rnums):
                rid = rnum_id_map.get(rnum)
                if rid is None:
                    continue
                price  = room_map.get(rnum, {}).get("price", 0)
                amount = price * nights
                cur.execute(
                    """INSERT INTO dbo.booking_detail
                           (booking_detail_id, booking_id, room_id, quantity, price, amount)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (bid * 1000 + idx + 1, bid, rid, nights, price, amount),
                )

        for p in data.get("payments", []):
            pd_id      = helpers.pay_to_int(p["id"])
            p_bid      = helpers.bk_to_int(p.get("bookingId", "BK-0"))
            cashier_id = emp_name_to_id.get(p.get("cashier", ""))
            cur.execute(
                """INSERT INTO dbo.payment_detail
                       (payment_detail_id, cashier_id, payment_id,
                        total_payment, payment_method, payment_datetime)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (pd_id, cashier_id, p_bid,
                 p.get("amount", 0), p.get("method", ""),
                 p.get("datetime") or None),
            )

        for pl in data.get("priceLogs", []):
            rid = rnum_id_map.get(pl["roomNumber"])
            if rid is None:
                continue
            cur.execute(
                """INSERT INTO dbo.room_log_price
                       (id, room_id, using_form_datetime, using_to_datetime, price_per_night)
                   VALUES (%s, %s, %s, %s, %s)""",
                (pl["id"], rid,
                 pl.get("from") or None, pl.get("to") or None,
                 pl["price"]),
            )

        for n in data.get("notifications", []):
            cur.execute(
                """INSERT INTO dbo.notifications
                       (id, title, sub, time_str, unread, icon)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (n["id"], n["title"], n.get("sub", ""), n.get("time", ""),
                 1 if n.get("unread", True) else 0, n.get("icon", "🔔")),
            )

        for name, value in data.get("counters", {}).items():
            cur.execute(
                "INSERT INTO dbo.counters (name, value) VALUES (%s, %s)",
                (name, value),
            )

        conn.commit()
        cur.close()
        return {"ok": True}

    except Exception as e:
        conn.rollback()
        import traceback; traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        conn.close()


# ── POST /api/state/reset ─────────────────────────────────────────────────────

@router.post("/api/state/reset")
def reset_state():
    conn = db.get_connection()
    try:
        cur = conn.cursor(as_dict=True)
        ensure_extras(cur)
        for tbl in DELETE_ORDER:
            cur.execute(f"DELETE FROM {tbl}")
        conn.commit()
        cur.close()
        return {"ok": True}
    except Exception as e:
        conn.rollback()
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        conn.close()
