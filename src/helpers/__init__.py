from datetime import date, datetime
from decimal import Decimal


def val(v):
    if v is None:               return None
    if isinstance(v, Decimal):  return float(v)
    if isinstance(v, datetime): return v.strftime("%Y-%m-%dT%H:%M")
    if isinstance(v, date):     return v.isoformat()
    return v


def bk_to_int(bid: str) -> int:
    return int(str(bid).replace("BK-", ""))

def int_to_bk(n) -> str:
    return f"BK-{n}"

def pay_to_int(pid: str) -> int:
    return int(str(pid).replace("PAY-", ""))

def int_to_pay(n) -> str:
    return f"PAY-{n}"

def emp_to_int(eid: str) -> int:
    return int(str(eid).replace("EMP-", "").lstrip("0") or "0")

def int_to_emp(n) -> str:
    return f"EMP-{str(n).zfill(3)}"

def rnum_to_id(num: str) -> int:
    return int(str(num))

def is_avail_to_status(v) -> str:
    if v is None: return "maintenance"
    v = float(v)
    if v == 1.0:  return "available"
    if v == 0.0:  return "occupied"
    return "maintenance"
