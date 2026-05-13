from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class DashboardKpiToday(BaseModel):
    total_bookings_today: Optional[int] = None
    total_revenue_today: Optional[float] = None
    total_customers_today: Optional[int] = None
    total_active_rooms: Optional[int] = None
    occupied_rooms_today: Optional[int] = None
    occupancy_rate_pct: Optional[float] = None
    report_date: Optional[date] = None


class DashboardRecentBookingRow(BaseModel):
    booking_detail_id: int
    booking_id: int
    booking_created_at: Optional[datetime] = None
    customer_id: int
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    room_num: Optional[str] = None
    room_name: Optional[str] = None
    room_type: Optional[str] = None
    hotel_name: Optional[str] = None
    checkin_date: Optional[date] = None
    checkout_date: Optional[date] = None
    quantity_of_nights: Optional[int] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None
    is_fully_paid: Optional[bool] = None


class DashboardRevenue7DayRow(BaseModel):
    revenue_date: Optional[date] = None
    day_name: Optional[str] = None
    total_bookings: Optional[int] = None
    total_customers: Optional[int] = None
    room_revenue: Optional[float] = None
    service_revenue: Optional[float] = None
    total_revenue: Optional[float] = None


class DashboardRoomTypeDistributionRow(BaseModel):
    room_type_id: int
    room_type_name: Optional[str] = None
    total_rooms: Optional[int] = None
    booked_rooms: Optional[int] = None
    available_rooms: Optional[int] = None
    room_type_pct: Optional[float] = None
    occupancy_rate_pct: Optional[float] = None


class DashboardTopCustomerRow(BaseModel):
    customer_id: int
    customer_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    membership_name: Optional[str] = None
    total_bookings: Optional[int] = None
    total_nights: Optional[int] = None
    total_paid: Optional[float] = None
    total_booking_amount: Optional[float] = None
    last_booking_date: Optional[date] = None
    customer_tier: Optional[str] = None
