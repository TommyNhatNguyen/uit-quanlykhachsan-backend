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
                INSERT INTO dbo.employee (employee_id, employee_name, birthday, phone, is_working, position, start_working_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (employee.employee_id, employee.employee_name, employee.birthday, employee.phone, employee.is_working, employee.position, employee.start_working_date))
            conn.commit()
            return self.get_employee(employee.employee_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_employee(self, employee_id: int) -> Employee:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.employee WHERE employee_id = %s
            """, (employee_id,))
            return Employee(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_employee(self, employee: UpdateEmployee) -> Employee:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.employee SET employee_name = %s, birthday = %s, phone = %s, is_working = %s, position = %s, start_working_date = %s WHERE employee_id = %s
            """, (employee.employee_name, employee.birthday, employee.phone, employee.is_working, employee.position, employee.start_working_date, employee.employee_id))
            conn.commit()
            return self.get_employee(employee.employee_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_employee(self, employee_id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.employee WHERE employee_id = %s
            """, (employee_id,))
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
                SELECT * FROM dbo.employee
                ORDER BY employee_id
                OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return {"page": page, "page_size": page_size, "total": total, "total_pages": total_pages, "data": [Employee(**row) for row in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
