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
from src.db.utils import ensure_extras, ensure_reference_data
from src.routers import api_state

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        conn = db.get_connection()
        cur = conn.cursor(as_dict=True)
        ensure_extras(cur)
        ensure_reference_data(cur)
        conn.commit()
        cur.close()
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


@app.get("/")
def index():
    return FileResponse(os.path.join(BASE_DIR, "admin.html"))

app.include_router(api_state.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
