import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.notification import Notification, CreateNotification, UpdateNotification


class NotificationRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_notification(self, notification: CreateNotification) -> Notification:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.notifications (id, title, sub, time_str, unread, icon)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (notification.id, notification.title, notification.sub, notification.time_str, notification.unread, notification.icon))
            conn.commit()
            return self.get_notification(notification.id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_notification(self, id: int) -> Notification:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.notifications WHERE id = %s
            """, (id,))
            return Notification(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_notification(self, notification: UpdateNotification) -> Notification:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.notifications SET title = %s, sub = %s, time_str = %s, unread = %s, icon = %s WHERE id = %s
            """, (notification.title, notification.sub, notification.time_str, notification.unread, notification.icon, notification.id))
            conn.commit()
            return self.get_notification(notification.id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_notification(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.notifications WHERE id = %s
            """, (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_notifications(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.notifications
                ORDER BY id DESC
                OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return {"page": page, "page_size": page_size, "total": total, "total_pages": total_pages, "data": [Notification(**row) for row in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
