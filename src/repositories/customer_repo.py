import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.customer import Customer, CreateCustomer, UpdateCustomer


class CustomerRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_customer(self, customer: CreateCustomer) -> Customer:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.customer (name, phone, sex, identification_id, email, birthday, membership_type_id)
                OUTPUT INSERTED.id VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (customer.name, customer.phone, customer.sex, customer.identification_id,
                  customer.email, customer.birthday, customer.membership_type_id))
            new_id = cur.fetchone()["id"]
            conn.commit()
            return self.get_customer(new_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_customer(self, id: int) -> Customer:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.customer WHERE id = %s", (id,))
            return Customer(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_customer(self, id: int, customer: Customer) -> Customer:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.customer SET name=%s, phone=%s, sex=%s, identification_id=%s,
                    email=%s, birthday=%s, membership_type_id=%s WHERE id=%s
            """, (customer.name, customer.phone, customer.sex, customer.identification_id,
                  customer.email, customer.birthday, customer.membership_type_id, id))
            conn.commit()
            return self.get_customer(id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_customer(self, id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("DELETE FROM dbo.customer WHERE id=%s", (id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_customers(self, page: int = 1, page_size: int = 10) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.customer
                ORDER BY id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, ((page - 1) * page_size, page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            return {"page": page, "page_size": page_size, "total": total,
                    "total_pages": math.ceil(total / page_size) if total else 0,
                    "data": [Customer(**r) for r in rows]}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
