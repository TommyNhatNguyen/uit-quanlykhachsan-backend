"""
HotelBooking Admin — FastAPI REST API
"""
from contextlib import asynccontextmanager
import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from src.db.db import db
from src.routers import (
    booking_router,
    booking_detail_router,
    customer_router,
    customer_history_purchase_router,
    employee_router,
    employee_account_router,
    hotel_router,
    membership_type_router,
    payment_router,
    room_router,
    room_log_price_router,
    room_type_router,
    service_detail_router,
    service_item_router,
    service_price_log_router,
    stats_router,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        conn = db.get_connection()
        conn.close()
        print("✅  Kết nối SQL Server thành công")
    except Exception as e:
        print(f"❌  Lỗi kết nối: {e}")
        raise
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hotel_router.router)
app.include_router(room_type_router.router)
app.include_router(room_router.router)
app.include_router(room_log_price_router.router)
app.include_router(customer_router.router)
app.include_router(membership_type_router.router)
app.include_router(employee_account_router.router)
app.include_router(employee_router.router)

app.include_router(booking_router.router)
app.include_router(booking_detail_router.router)
app.include_router(customer_history_purchase_router.router)
app.include_router(payment_router.router)
app.include_router(stats_router.router)
app.include_router(service_detail_router.router)
app.include_router(service_item_router.router)
app.include_router(service_price_log_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
