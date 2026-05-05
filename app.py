"""
HotelBooking Admin — Flask REST API
Backend kết nối SQL Server theo schema CLAUDE.md.
"""
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pymssql
from datetime import date, datetime
from decimal import Decimal
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── DB Config ────────────────────────────────────────────────────────────────

DB_CONFIG = {
    "server":   "165.22.106.126",
    "port":     1433,
    "database": "master",
    "user":     "sa",
    "password": "Uit123@abc",
    "charset":  "utf8",
}


def get_db():
    return pymssql.connect(**DB_CONFIG)


# ─── ID helpers ───────────────────────────────────────────────────────────────

def bk_to_int(bid: str) -> int:
    return int(str(bid).replace("BK-", ""))

def int_to_bk(n) -> str:
    return f"BK-{n}"

def pay_to_int(pid: str) -> int:
    return int(str(pid).replace("PAY-", ""))

def int_to_pay(n) -> str:
    return f"PAY-{n}"

def emp_to_int(eid: str) -> int:
    return int(str(eid).replace("EMP-", "").lstrip("0") or "0")

def int_to_emp(n) -> str:
    return f"EMP-{str(n).zfill(3)}"

def rnum_to_id(num: str) -> int:
    return int(str(num))

TIER_ID  = {"Silver": 1, "Gold": 2, "Diamond": 3}
RTYPE_ID = {"Standard": 1, "Deluxe": 2, "Suite": 3, "Family": 4}
IS_AVAIL = {"available": 1.0, "occupied": 0.0, "maintenance": -1.0}

def is_avail_to_status(v) -> str:
    if v is None: return "maintenance"
    v = float(v)
    if v == 1.0:  return "available"
    if v == 0.0:  return "occupied"
    return "maintenance"


# ─── Value coercion for JSON ──────────────────────────────────────────────────

def _val(v):
    if v is None: return None
    if isinstance(v, Decimal):  return float(v)
    if isinstance(v, datetime): return v.strftime("%Y-%m-%dT%H:%M")
    if isinstance(v, date):     return v.isoformat()
    return v


# ─── Ensure extra tables / columns ───────────────────────────────────────────

def _ensure_extras(cur):
    cur.execute("""
        IF OBJECT_ID(N'dbo.notifications', 'U') IS NULL
        CREATE TABLE dbo.notifications (
            id        BIGINT        PRIMARY KEY,
            title     NVARCHAR(255) NOT NULL,
            sub       NVARCHAR(MAX) DEFAULT '',
            time_str  NVARCHAR(100) DEFAULT '',
            unread    BIT           DEFAULT 1,
            icon      NVARCHAR(50)  DEFAULT N'🔔'
        )
    """)
    cur.execute("""
        IF OBJECT_ID(N'dbo.counters', 'U') IS NULL
        CREATE TABLE dbo.counters (
            name  NVARCHAR(100) PRIMARY KEY,
            value INT           NOT NULL DEFAULT 0
        )
    """)
    cur.execute("""
        IF COL_LENGTH('dbo.booking', 'notes') IS NULL
        ALTER TABLE dbo.booking ADD notes NVARCHAR(MAX) DEFAULT ''
    """)
    cur.execute("""
        IF COL_LENGTH('dbo.service_item', 'used_count') IS NULL
        ALTER TABLE dbo.service_item ADD used_count INT DEFAULT 0
    """)


def _ensure_reference_data(cur):
    cur.execute("SELECT COUNT(*) AS cnt FROM dbo.membership_type")
    if cur.fetchone()["cnt"] == 0:
        cur.execute("INSERT INTO dbo.membership_type VALUES (1, N'Silver', 0, 20000000)")
        cur.execute("INSERT INTO dbo.membership_type VALUES (2, N'Gold', 20000000, 50000000)")
        cur.execute("INSERT INTO dbo.membership_type VALUES (3, N'Diamond', 50000000, NULL)")

    cur.execute("SELECT COUNT(*) AS cnt FROM dbo.room_type")
    if cur.fetchone()["cnt"] == 0:
        cur.execute("INSERT INTO dbo.room_type VALUES (1, N'Standard')")
        cur.execute("INSERT INTO dbo.room_type VALUES (2, N'Deluxe')")
        cur.execute("INSERT INTO dbo.room_type VALUES (3, N'Suite')")
        cur.execute("INSERT INTO dbo.room_type VALUES (4, N'Family')")

    cur.execute("SELECT COUNT(*) AS cnt FROM dbo.counters")
    if cur.fetchone()["cnt"] == 0:
        for name, value in [
            ("booking", 2105), ("customer", 9), ("service", 12),
            ("employee", 9),   ("payment", 3302), ("price", 105),
        ]:
            cur.execute(
                "INSERT INTO dbo.counters (name, value) VALUES (%s, %s)",
                (name, value),
            )


# ─── FK-safe delete order (children before parents) ──────────────────────────

DELETE_ORDER = [
    "dbo.customer_history_purchase",
    "dbo.service_detail",
    "dbo.payment_detail",
    "dbo.booking_detail",
    "dbo.room_log_price",
    "dbo.room_inventory_log",
    "dbo.booking",
    "dbo.payment",
    "dbo.room",
    "dbo.room_inventory",
    "dbo.customer",
    "dbo.employee",
    "dbo.service_item",
    "dbo.membership_type",
    "dbo.room_type",
    "dbo.notifications",
    "dbo.counters",
]


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "admin.html")


# ── GET /api/state ────────────────────────────────────────────────────────────

@app.route("/api/state", methods=["GET"])
def get_state():
    conn = get_db()
    try:
        cur = conn.cursor(as_dict=True)
        _ensure_extras(cur)
        _ensure_reference_data(cur)
        conn.commit()

        # ── Bookings ──────────────────────────────────────────────────────────
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
                "id":         int_to_bk(r["booking_id"]),
                "customerId": r["customer_id"],
                "customer":   r["customer_name"],
                "checkin":    _val(r["checkin"])  or "",
                "checkout":   _val(r["checkout"]) or "",
                "rooms":      r["rooms"] or "",
                "status":     (r["status"] or "pending").lower(),
                "payment":    (r["payment_status"] or "unpaid").lower(),
                "amount":     float(r["total_amount"] or 0),
                "notes":      r["notes"] or "",
            }
            for r in cur.fetchall()
        ]

        # ── Customers ─────────────────────────────────────────────────────────
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
                "dob":       _val(r["birthday"]) or "",
                "tier":      r["tier"] or "Silver",
                "totalPaid": float(r["total_paid"] or 0),
                "notes":     "",
            }
            for r in cur.fetchall()
        ]

        # ── Rooms ─────────────────────────────────────────────────────────────
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
                "status":   is_avail_to_status(r["is_available"]),
            }
            for r in cur.fetchall()
        ]

        # ── Services ──────────────────────────────────────────────────────────
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

        # ── Employees ─────────────────────────────────────────────────────────
        cur.execute("""
            SELECT employee_id, employee_name, birthday, phone,
                   is_working, position, start_working_date
            FROM dbo.employee
            ORDER BY employee_id
        """)
        employees = [
            {
                "id":       int_to_emp(r["employee_id"]),
                "name":     r["employee_name"],
                "dob":      _val(r["birthday"]) or "",
                "phone":    r["phone"] or "",
                "position": r["position"] or "",
                "start":    _val(r["start_working_date"]) or "",
                "working":  str(r["is_working"]).lower() == "true",
            }
            for r in cur.fetchall()
        ]

        # ── Payments ──────────────────────────────────────────────────────────
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
                "id":        int_to_pay(r["payment_detail_id"]),
                "bookingId": int_to_bk(r["booking_id"]),
                "customer":  r["customer_name"],
                "method":    r["payment_method"] or "",
                "cashier":   r["cashier"] or "",
                "datetime":  _val(r["payment_datetime"]) or "",
                "amount":    float(r["total_payment"] or 0),
                "status":    (r["status"] or "success").lower(),
            }
            for r in cur.fetchall()
        ]

        # ── Price logs ────────────────────────────────────────────────────────
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
                "from":       _val(r["using_form_datetime"]) or "",
                "to":         _val(r["using_to_datetime"]),
                "price":      float(r["price_per_night"] or 0),
            }
            for r in cur.fetchall()
        ]

        # ── Notifications ─────────────────────────────────────────────────────
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

        # ── Counters ──────────────────────────────────────────────────────────
        cur.execute("SELECT * FROM dbo.counters")
        counters = {r["name"]: r["value"] for r in cur.fetchall()}

        cur.close()
        return jsonify({
            "bookings":      bookings,
            "customers":     customers,
            "rooms":         rooms,
            "services":      services,
            "employees":     employees,
            "payments":      payments,
            "priceLogs":     price_logs,
            "notifications": notifications,
            "counters":      counters,
        })
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


# ── PUT /api/state ────────────────────────────────────────────────────────────

@app.route("/api/state", methods=["PUT"])
def save_state():
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "No JSON body"}), 400

    conn = get_db()
    try:
        cur = conn.cursor(as_dict=True)
        _ensure_extras(cur)

        for tbl in DELETE_ORDER:
            cur.execute(f"DELETE FROM {tbl}")

        # ── Reference tables ──────────────────────────────────────────────────
        cur.execute("INSERT INTO dbo.membership_type VALUES (1, N'Silver', 0, 20000000)")
        cur.execute("INSERT INTO dbo.membership_type VALUES (2, N'Gold', 20000000, 50000000)")
        cur.execute("INSERT INTO dbo.membership_type VALUES (3, N'Diamond', 50000000, NULL)")
        cur.execute("INSERT INTO dbo.room_type VALUES (1, N'Standard')")
        cur.execute("INSERT INTO dbo.room_type VALUES (2, N'Deluxe')")
        cur.execute("INSERT INTO dbo.room_type VALUES (3, N'Suite')")
        cur.execute("INSERT INTO dbo.room_type VALUES (4, N'Family')")

        # ── Customers ─────────────────────────────────────────────────────────
        for c in data.get("customers", []):
            cur.execute(
                """INSERT INTO dbo.customer
                       (customer_id, customer_name, sex, phone, email, birthday,
                        membership_type_id, total_paid)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (c["id"], c["name"], c.get("sex", ""), c.get("phone", ""),
                 c.get("email", ""), c.get("dob") or None,
                 TIER_ID.get(c.get("tier", "Silver"), 1), c.get("totalPaid", 0)),
            )

        # ── Employees ─────────────────────────────────────────────────────────
        emp_name_to_id: dict = {}
        for e in data.get("employees", []):
            eid = emp_to_int(e["id"])
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

        # ── Services ──────────────────────────────────────────────────────────
        for s in data.get("services", []):
            cur.execute(
                """INSERT INTO dbo.service_item
                       (service_item_id, service_item_name, catalog, price, used_count)
                   VALUES (%s, %s, %s, %s, %s)""",
                (s["id"], s["name"], s["catalog"], s["price"], s.get("used", 0)),
            )

        # ── Rooms: room_inventory first (room has FK to it), then room ────────
        rnum_id_map: dict = {}
        for r in data.get("rooms", []):
            rid     = rnum_to_id(r["number"])
            rnum_id_map[r["number"]] = rid
            type_id = RTYPE_ID.get(r["type"], 1)
            is_av   = IS_AVAIL.get(r.get("status", "available"), 1.0)

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

        # ── Bookings: payment → booking → booking_detail ──────────────────────
        room_map = {r["number"]: r for r in data.get("rooms", [])}

        for b in data.get("bookings", []):
            bid    = bk_to_int(b["id"])
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

        # ── Payment details ───────────────────────────────────────────────────
        for p in data.get("payments", []):
            pd_id      = pay_to_int(p["id"])
            p_bid      = bk_to_int(p.get("bookingId", "BK-0"))
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

        # ── Price logs ────────────────────────────────────────────────────────
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

        # ── Notifications ─────────────────────────────────────────────────────
        for n in data.get("notifications", []):
            cur.execute(
                """INSERT INTO dbo.notifications
                       (id, title, sub, time_str, unread, icon)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (n["id"], n["title"], n.get("sub", ""), n.get("time", ""),
                 1 if n.get("unread", True) else 0, n.get("icon", "🔔")),
            )

        # ── Counters ──────────────────────────────────────────────────────────
        for name, value in data.get("counters", {}).items():
            cur.execute(
                "INSERT INTO dbo.counters (name, value) VALUES (%s, %s)",
                (name, value),
            )

        conn.commit()
        cur.close()
        return jsonify({"ok": True})

    except Exception as e:
        conn.rollback()
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


# ── POST /api/state/reset ─────────────────────────────────────────────────────

@app.route("/api/state/reset", methods=["POST"])
def reset_state():
    conn = get_db()
    try:
        cur = conn.cursor(as_dict=True)
        _ensure_extras(cur)
        for tbl in DELETE_ORDER:
            cur.execute(f"DELETE FROM {tbl}")
        conn.commit()
        cur.close()
        return jsonify({"ok": True})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


# ─── Start ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        conn = get_db()
        cur = conn.cursor(as_dict=True)
        _ensure_extras(cur)
        _ensure_reference_data(cur)
        conn.commit()
        cur.close()
        conn.close()
        print("✅  Kết nối SQL Server thành công")
    except Exception as e:
        print(f"❌  Lỗi kết nối: {e}")
        raise

    print("✅  HotelBooking API → http://127.0.0.1:5001")
    app.run(debug=True, host="0.0.0.0", port=5001)
