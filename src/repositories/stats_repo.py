from fastapi.responses import JSONResponse

from src.db.db import MySQLDatabase
from src.models.stats import (
    DashboardKpiToday,
    DashboardRecentBookingRow,
    DashboardRevenue7DayRow,
    DashboardRoomTypeDistributionRow,
    DashboardTopCustomerRow,
)


class StatsRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def get_kpi_today(self) -> DashboardKpiToday | JSONResponse:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.vw_dashboard_kpi_today")
            row = cur.fetchone()
            if not row:
                return DashboardKpiToday()
            return DashboardKpiToday(**row)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_recent_bookings(self, limit: int) -> list[DashboardRecentBookingRow] | JSONResponse:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute(
                """
                SELECT TOP (%s) *
                FROM dbo.vw_dashboard_recent_bookings
                ORDER BY booking_created_at DESC
                """,
                (limit,),
            )
            rows = cur.fetchall() or []
            return [DashboardRecentBookingRow(**r) for r in rows]
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_revenue_7days(self) -> list[DashboardRevenue7DayRow] | JSONResponse:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute(
                """
                SELECT * FROM dbo.vw_dashboard_revenue_7days
                ORDER BY revenue_date
                """
            )
            rows = cur.fetchall() or []
            return [DashboardRevenue7DayRow(**r) for r in rows]
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_room_type_distribution(self) -> list[DashboardRoomTypeDistributionRow] | JSONResponse:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.vw_dashboard_room_type_distribution")
            rows = cur.fetchall() or []
            return [DashboardRoomTypeDistributionRow(**r) for r in rows]
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_top_customers(self, limit: int) -> list[DashboardTopCustomerRow] | JSONResponse:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute(
                """
                SELECT TOP (%s) *
                FROM dbo.vw_dashboard_top_customers
                ORDER BY total_paid DESC, total_bookings DESC
                """,
                (limit,),
            )
            rows = cur.fetchall() or []
            return [DashboardTopCustomerRow(**r) for r in rows]
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
