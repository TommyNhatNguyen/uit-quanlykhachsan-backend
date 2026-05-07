import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.room_price_log import QueryRoomPriceLogsParams, RoomPriceLog, PopulatedRoomPriceLog, CreateRoomPriceLog, UpdateRoomPriceLog
from src.models.room import Room


class RoomPriceLogRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_room_price_log(self, log: CreateRoomPriceLog) -> RoomPriceLog:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.room_price_log (room_id, created_at, price_per_night)
                OUTPUT INSERTED.id VALUES (%s, %s, %s)
            """, (log.room_id, log.created_at, log.price_per_night))
            new_id = cur.fetchone()["id"]
            conn.commit()
            return self.get_room_price_log(new_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_room_price_log(self, id: int) -> RoomPriceLog:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.room_price_log WHERE id = %s", (id,))
            return RoomPriceLog(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_room_price_log(self, id: int, log: RoomPriceLog) -> RoomPriceLog:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.room_price_log SET room_id=%s, created_at=%s, price_per_night=%s WHERE id=%s
            """, (log.room_id, log.created_at, log.price_per_night, id))
            conn.commit()
            return self.get_room_price_log(id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_room_price_log(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("DELETE FROM dbo.room_price_log WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_room_price_logs(self, params: QueryRoomPriceLogsParams) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)

            where = "WHERE 1=1"
            filter_args = []
            if params.room_id:
                where += " AND room_id = %s"
                filter_args.append(params.room_id)

            cur.execute(f"SELECT COUNT(*) AS total FROM dbo.room_price_log {where}", filter_args)
            total = cur.fetchone()["total"]

            cur.execute(f"""
                SELECT rpl.id, rpl.room_id, rpl.created_at, rpl.price_per_night,
                    r.id AS r_id, r.room_num AS r_room_num, r.room_name AS r_room_name,
                    r.capacity AS r_capacity, r.area AS r_area, r.is_smoking AS r_is_smoking,
                    r.has_wifi AS r_has_wifi, r.has_pool AS r_has_pool,
                    r.description AS r_description, r.room_type_id AS r_room_type_id,
                    r.hotel_id AS r_hotel_id,
                    r.current_price_per_night AS r_current_price_per_night,
                    r.is_deleted AS r_is_deleted,
                    r.is_underconstruction AS r_is_underconstruction
                FROM dbo.room_price_log rpl
                LEFT JOIN dbo.room r ON rpl.room_id = r.id
                {where}
                ORDER BY r.id ASC, rpl.created_at DESC OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, filter_args + [(params.page - 1) * params.page_size, params.page_size])
            rows = cur.fetchall()

            data = []
            for row in rows:
                room = None
                if row.get("r_id"):
                    room_data = {k[2:]: v for k, v in row.items() if k.startswith("r_")}
                    room = Room(**room_data)
                log_data = {k: v for k, v in row.items() if not k.startswith("r_")}
                data.append(PopulatedRoomPriceLog(**log_data, room=room))

            return {"page": params.page, "page_size": params.page_size, "total": total,
                    "total_pages": math.ceil(total / params.page_size) if total else 0,
                    "data": data}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
