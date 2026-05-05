import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.customer import Customer, CreateCustomer, UpdateCustomer
from src.models.paginate_model import PaginateModel


class CustomerRepository:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def create_customer(self, customer: CreateCustomer) -> Customer:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                INSERT INTO dbo.customer (customer_id, customer_name, sex, phone, email, birthday, membership_type_id, total_paid)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (customer.customer_id, customer.customer_name, customer.sex, customer.phone, customer.email, customer.birthday, customer.membership_type_id, customer.total_paid))
            conn.commit()
            return self.get_customer(customer.customer_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_customer(self, customer_id: int) -> Customer:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.customer WHERE customer_id = %s
            """, (customer_id,))
            return Customer(**cur.fetchone())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def update_customer(self, customer: UpdateCustomer) -> Customer:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                UPDATE dbo.customer SET customer_name = %s, sex = %s, phone = %s, email = %s, birthday = %s, membership_type_id = %s, total_paid = %s WHERE customer_id = %s
            """, (customer.customer_name, customer.sex, customer.phone, customer.email, customer.birthday, customer.membership_type_id, customer.total_paid, customer.customer_id))
            conn.commit()
            return self.get_customer(customer.customer_id)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def delete_customer(self, customer_id: int) -> bool:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                DELETE FROM dbo.customer WHERE customer_id = %s
            """, (customer_id,))
            conn.commit()
            return True
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()

    def get_list_customers(self, page: int = 1, page_size: int = 10) -> PaginateModel[Customer]:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)
            cur.execute("""
                SELECT * FROM dbo.customer
                LIMIT %s OFFSET %s
            """, (page_size, (page - 1) * page_size))
            rows = cur.fetchall()
            total = cur.rowcount
            total_pages = math.ceil(total / page_size)
            return PaginateModel[Customer](page=page, page_size=page_size, total=total, total_pages=total_pages, data=[Customer(**row) for row in rows])
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
