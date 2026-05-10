from ast import List
import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.room import QueryRoomsParams, AvailableRoomsParams, Room, PopulatedRoom, CreateRoom, UpdateRoom
from src.models.room_price_log import RoomPriceLog
from src.models.room_type import RoomType


class RoomRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_room(self, room: CreateRoom) -> Room:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DECLARE @Inserted TABLE (id INT);

                INSERT INTO dbo.room (
                    room_num,
                    room_name,
                    capacity,
                    area,
                    is_smoking,
                    has_wifi,
                    has_pool,
                    description,
                    room_type_id,
                    hotel_id,
                    current_price_per_night,
                    is_deleted,
                    is_underconstruction
                )
                OUTPUT INSERTED.id INTO @Inserted
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, 0, %s
                );

                SELECT id FROM @Inserted;
            """, (
                room.room_num,
                room.room_name,
                room.capacity,
                room.area,
                room.is_smoking,
                room.has_wifi,
                room.has_pool,
                room.description,
                room.room_type_id,
                room.hotel_id,
                room.current_price_per_night,
                room.is_underconstruction
            ))
            new_id = cur.fetchone()["id"]
            conn.commit()
            return self.get_room(new_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_room(self, id: int) -> Room:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.room WHERE id = %s", (id,))
            return Room(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_room(self, id: int, room: Room) -> Room:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.room SET room_num=%s, room_name=%s, capacity=%s, area=%s, is_smoking=%s,
                    has_wifi=%s, has_pool=%s, description=%s, room_type_id=%s, hotel_id=%s,
                    current_price_per_night=%s, is_deleted=%s, is_underconstruction=%s
                WHERE id=%s
            """, (room.room_num, room.room_name, room.capacity, room.area, room.is_smoking,
                  room.has_wifi, room.has_pool, room.description, room.room_type_id, room.hotel_id,
                  room.current_price_per_night, room.is_deleted, room.is_underconstruction, id))
            conn.commit()
            return self.get_room(id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_room(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("UPDATE dbo.room SET is_deleted=1 WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_rooms(self, params: QueryRoomsParams) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)

            where = "WHERE r.is_deleted=0"
            filter_args = []
            if params.room_type_id:
                where += " AND r.room_type_id = %s"
                filter_args.append(params.room_type_id)
            if params.price_from is not None and params.price_to is not None:
                where += " AND r.current_price_per_night >= %s AND r.current_price_per_night <= %s"
                filter_args.extend([params.price_from, params.price_to])

            cur.execute(f"SELECT COUNT(*) AS total FROM dbo.room r {where}", filter_args)
            total = cur.fetchone()["total"]

            cur.execute(f"""
                SELECT r.id, r.room_num, r.room_name, r.capacity, r.area, r.is_smoking,
                    r.has_wifi, r.has_pool, r.description, r.room_type_id, r.hotel_id,
                    r.current_price_per_night, r.is_deleted, r.is_underconstruction,
                    rt.id AS rt_id, rt.name AS rt_name, rt.is_deleted AS rt_is_deleted
                FROM dbo.room r
                LEFT JOIN dbo.room_type rt ON r.room_type_id = rt.id
                {where}
                ORDER BY r.id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, filter_args + [(params.page - 1) * params.page_size, params.page_size])
            rows = cur.fetchall()

            data = []
            for row in rows:
                room_type = None
                if row.get("rt_id"):
                    room_type = RoomType(id=row["rt_id"], name=row["rt_name"], is_deleted=row["rt_is_deleted"])
                room_data = {k: v for k, v in row.items() if not k.startswith("rt_")}
                data.append(PopulatedRoom(**room_data, room_type=room_type))

            return {"page": params.page, "page_size": params.page_size, "total": total,
                    "total_pages": math.ceil(total / params.page_size) if total else 0,
                    "data": data}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_available_rooms(self, params: AvailableRoomsParams) -> list:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                EXEC getAvailableRooms @p_checkin_date = %s, @p_checkout_date = %s;
            """, (params.checkin_date, params.checkout_date))
            return [Room(**r) for r in cur.fetchall()]
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_room_history_prices(self, id: int):
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            
            cur.execute("""
                EXEC getListPriceByRoomId @p_room_id = %s;
            """, (id))
          
            rows = cur.fetchall()

            data = []
            for row in rows:
                data.append(RoomPriceLog(**row))

            return data
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()