import math
from fastapi.responses import JSONResponse
from src.db.db import MySQLDatabase
from src.models.customer import Customer, PopulatedCustomer, CreateCustomer, UpdateCustomer, QueryCustomersParams
from src.models.membership import Membership


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

    def get_list_customers(self, params: QueryCustomersParams) -> dict:
        try:
            conn = self.db.get_connection()
            cur = conn.cursor(as_dict=True)

            where = "WHERE 1=1"
            filter_args = []
            if params.membership_type_id:
                where += " AND c.membership_type_id = %s"
                filter_args.append(params.membership_type_id)

            cur.execute(f"SELECT COUNT(*) AS total FROM dbo.customer c {where}", filter_args)
            total = cur.fetchone()["total"]

            cur.execute(f"""
                SELECT c.id, c.name, c.phone, c.sex, c.identification_id, c.email,
                    c.birthday, c.membership_type_id,
                    m.id AS m_id, m.name AS m_name, m.paid_from AS m_paid_from,
                    m.paid_to AS m_paid_to, m.is_deleted AS m_is_deleted
                FROM dbo.customer c
                LEFT JOIN dbo.membership m ON c.membership_type_id = m.id
                {where}
                ORDER BY c.id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
            """, filter_args + [(params.page - 1) * params.page_size, params.page_size])
            rows = cur.fetchall()

            data = []
            for row in rows:
                membership = None
                if row.get("m_id"):
                    membership_data = {k[2:]: v for k, v in row.items() if k.startswith("m_")}
                    membership = Membership(**membership_data)
                customer_data = {k: v for k, v in row.items() if not k.startswith("m_")}
                data.append(PopulatedCustomer(**customer_data, membership_type=membership))

            return {"page": params.page, "page_size": params.page_size, "total": total,
                    "total_pages": math.ceil(total / params.page_size) if total else 0,
                    "data": data}
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
        finally:
            conn.close()
