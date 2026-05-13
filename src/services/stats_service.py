from typing import TypeVar

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from src.models.stats import (
    DashboardKpiToday,
    DashboardRecentBookingRow,
    DashboardRevenue7DayRow,
    DashboardRoomTypeDistributionRow,
    DashboardTopCustomerRow,
)
from src.repositories.stats_repo import StatsRepository

_LIMIT_CAP = 200

T = TypeVar("T")


def _clamp_limit(limit: int, default: int) -> int:
    if limit < 1:
        return default
    return min(limit, _LIMIT_CAP)


class StatsService:
    def __init__(self, repo: StatsRepository):
        self.repo = repo

    @staticmethod
    def _unwrap(result: T | JSONResponse) -> T:
        if isinstance(result, JSONResponse):
            body = getattr(result, "body", None) or b"{}"
            try:
                import json

                detail = json.loads(body.decode()).get("error", "Database error")
            except Exception:
                detail = "Database error"
            raise HTTPException(status_code=500, detail=detail)
        return result  # type: ignore[return-value]

    def get_kpi_today(self) -> DashboardKpiToday:
        return self._unwrap(self.repo.get_kpi_today())

    def get_recent_bookings(self, limit: int = 50) -> list[DashboardRecentBookingRow]:
        n = _clamp_limit(limit, 50)
        return self._unwrap(self.repo.get_recent_bookings(n))

    def get_revenue_7days(self) -> list[DashboardRevenue7DayRow]:
        return self._unwrap(self.repo.get_revenue_7days())

    def get_room_type_distribution(self) -> list[DashboardRoomTypeDistributionRow]:
        return self._unwrap(self.repo.get_room_type_distribution())

    def get_top_customers(self, limit: int = 20) -> list[DashboardTopCustomerRow]:
        n = _clamp_limit(limit, 20)
        return self._unwrap(self.repo.get_top_customers(n))
