import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.employee import Employee, CreateEmployee, UpdateEmployee


class EmployeeRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_employee(self, employee: CreateEmployee) -> Employee:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.employee (name, phone, start_working_date, is_deleted)
                OUTPUT INSERTED.id VALUES (%s, %s, %s, 0)
            """, (employee.name, employee.phone, employee.start_working_date))
            new_id = cur.fetchone()["id"]
            conn.commit()
            return self.get_employee(new_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_employee(self, id: int) -> Employee:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.employee WHERE id = %s", (id,))
            return Employee(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_employee(self, id: int, employee: Employee) -> Employee:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.employee SET name=%s, birthday=%s, phone=%s, is_working=%s, position=%s,
                    start_working_date=%s, employee_account_id=%s, is_deleted=%s, role=%s WHERE id=%s
            """, (employee.name, employee.birthday, employee.phone, employee.is_working, employee.position,
                  employee.start_working_date, employee.employee_account_id, employee.is_deleted,
                  employee.role, id))
            conn.commit()
            return self.get_employee(id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_employee(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("UPDATE dbo.employee SET is_deleted=1 WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_employees(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.employee WHERE is_deleted=0
                ORDER BY id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            return {"page": page, "page_size": page_size, "total": total,
                    "total_pages": math.ceil(total / page_size) if total else 0,
                    "data": [Employee(**r) for r in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
