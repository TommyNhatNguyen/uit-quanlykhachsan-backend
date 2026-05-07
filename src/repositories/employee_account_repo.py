import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.employee_account import EmployeeAccount, CreateEmployeeAccount, UpdateEmployeeAccount


class EmployeeAccountRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_employee_account(self, account: CreateEmployeeAccount) -> EmployeeAccount:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.employee_account (username, password, created_at)
                OUTPUT INSERTED.id VALUES (%s, %s, %s)
            """, (account.username, account.password, account.created_at))
            new_id = cur.fetchone()["id"]
            conn.commit()
            return self.get_employee_account(new_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_employee_account(self, id: int) -> EmployeeAccount:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.employee_account WHERE id = %s", (id,))
            return EmployeeAccount(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_employee_account(self, id: int, account: EmployeeAccount) -> EmployeeAccount:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.employee_account SET username=%s, password=%s, created_at=%s WHERE id=%s
            """, (account.username, account.password, account.created_at, id))
            conn.commit()
            return self.get_employee_account(id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_employee_account(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("DELETE FROM dbo.employee_account WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_by_credentials(self, username: str, password: str):
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute(
                "SELECT * FROM dbo.employee_account WHERE username=%s AND password=%s",
                (username, password)
            )
            row = cur.fetchone()
            if not row:
                return None
            return EmployeeAccount(**row)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_employee_accounts(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.employee_account
                ORDER BY id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            return {"page": page, "page_size": page_size, "total": total,
                    "total_pages": math.ceil(total / page_size) if total else 0,
                    "data": [EmployeeAccount(**r) for r in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
