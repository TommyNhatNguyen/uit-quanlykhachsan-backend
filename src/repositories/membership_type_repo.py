import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.membership import Membership, CreateMembership, UpdateMembership


class MembershipRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_membership(self, membership: CreateMembership) -> Membership:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.membership (name, paid_from, paid_to, is_deleted)
                OUTPUT INSERTED.id VALUES (%s, %s, %s, 0)
            """, (membership.name, membership.paid_from, membership.paid_to))
            new_id = cur.fetchone()["id"]
            conn.commit()
            return self.get_membership(new_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_membership(self, id: int) -> Membership:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.membership WHERE id = %s", (id,))
            return Membership(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_membership(self, id: int, membership: Membership) -> Membership:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.membership SET name=%s, paid_from=%s, paid_to=%s, is_deleted=%s WHERE id=%s
            """, (membership.name, membership.paid_from, membership.paid_to, membership.is_deleted, id))
            conn.commit()
            return self.get_membership(id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_membership(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("UPDATE dbo.membership SET is_deleted=1 WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_memberships(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.membership WHERE is_deleted=0
                ORDER BY id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            return {"page": page, "page_size": page_size, "total": total,
                    "total_pages": math.ceil(total / page_size) if total else 0,
                    "data": [Membership(**r) for r in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
