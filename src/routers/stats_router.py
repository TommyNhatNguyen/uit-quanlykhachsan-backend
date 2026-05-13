from fastapi import APIRouter

from src.db.db import db
from src.repositories.stats_repo import StatsRepository
from src.services.stats_service import StatsService

router = APIRouter(prefix="/api/stats", tags=["stats"])


def _svc() -> StatsService:
    return StatsService(StatsRepository(db))


@router.get("/kpi-today")
def get_kpi_today():
    return _svc().get_kpi_today()


@router.get("/recent-bookings")
def get_recent_bookings(limit: int = 50):
    return _svc().get_recent_bookings(limit)


@router.get("/revenue-7days")
def get_revenue_7days():
    return _svc().get_revenue_7days()


@router.get("/room-type-distribution")
def get_room_type_distribution():
    return _svc().get_room_type_distribution()


@router.get("/top-customers")
def get_top_customers(limit: int = 20):
    return _svc().get_top_customers(limit)
