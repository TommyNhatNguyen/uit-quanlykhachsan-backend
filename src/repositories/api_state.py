from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.customer import CreateCustomer, Customer


class ApiStateRepository:   
    def __init__(self, db: MySQLDatabase):
        self.db = db

    async def get_state(self) -> list[Customer]:
        conn = self.db.get_connection()
        try:
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.customer
            """)
            rows = cur.fetchall()
            customers = [Customer(**row) for row in rows]
            return customers
        except Exception as e:
            import traceback; traceback.print_exc()
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
    async def create_customer(self, customer: CreateCustomer) -> Customer:
        conn = self.db.get_connection()
        try:
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.customer (customer_id, customer_name, sex, phone, email, birthday, membership_type_id, total_paid)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
            """, (customer.customer_id, customer.customer_name, customer.sex, customer.phone, customer.email, customer.birthday, customer.membership_type_id, customer.total_paid))
            conn.commit()
            
            cur.execute("""
                SELECT * FROM dbo.customer WHERE customer_id = %s
            """, (customer.customer_id,))
            row = cur.fetchone()
            if row:
                return Customer(**row)
            else:
                return JSONResponse({"error": "Customer not created"}, status_code=400)
        except Exception as e:
            import traceback; traceback.print_exc()
            return JSONResponse({"error": str(e)}, status_code=500) 
        finally:
            conn.close()