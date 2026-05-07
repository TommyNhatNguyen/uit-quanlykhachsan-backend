from typing import Optional
from pydantic import BaseModel

from src.models.customer import PopulatedCustomer


class CustomerHistoryPurchase(BaseModel):
    id: int
    customer_id: Optional[int]
    booking_id: Optional[int]
    booking_paid: Optional[float]
    cumulative_paid: Optional[float]


class PopulatedCustomerHistoryPurchase(CustomerHistoryPurchase):
    customer: Optional[PopulatedCustomer] = None
    # TODO: Add booking
    # booking: Optional[PopulatedBooking] = None


class CreateCustomerHistoryPurchase(BaseModel):
    customer_id: int
    booking_id: int
    booking_paid: Optional[float] = None
    cumulative_paid: Optional[float] = None


class UpdateCustomerHistoryPurchase(BaseModel):
    customer_id: Optional[int] = None
    booking_id: Optional[int] = None
    booking_paid: Optional[float] = None
    cumulative_paid: Optional[float] = None