import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.membership_type import MembershipType, CreateMembershipType, UpdateMembershipType
from src.models.paginate_model import PaginateModel


class MembershipTypeRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_membership_type(self, membership_type: CreateMembershipType) -> MembershipType:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.membership_type (membership_type_id, membership_type_name, paid_from, paid_to)
                VALUES (%s, %s, %s, %s)
            """, (membership_type.membership_type_id, membership_type.membership_type_name, membership_type.paid_from, membership_type.paid_to))
            conn.commit()
            return self.get_membership_type(membership_type.membership_type_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_membership_type(self, membership_type_id: int) -> MembershipType:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.membership_type WHERE membership_type_id = %s
            """, (membership_type_id,))
            return MembershipType(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_membership_type(self, membership_type: UpdateMembershipType) -> MembershipType:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.membership_type SET membership_type_name = %s, paid_from = %s, paid_to = %s WHERE membership_type_id = %s
            """, (membership_type.membership_type_name, membership_type.paid_from, membership_type.paid_to, membership_type.membership_type_id))
            conn.commit()
            return self.get_membership_type(membership_type.membership_type_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_membership_type(self, membership_type_id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.membership_type WHERE membership_type_id = %s
            """, (membership_type_id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_membership_types(self, page: int = 1, page_size: int = 10) -> PaginateModel[MembershipType]:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.membership_type
                LIMIT %s OFFSET %s
            """, (page_size, (page - 1) * page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return PaginateModel[MembershipType](page=page, page_size=page_size, total=total, total_pages=total_pages, data=[MembershipType(**row) for row in rows])
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
