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


def ensure_extras(cur):
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


def ensure_reference_data(cur):
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
