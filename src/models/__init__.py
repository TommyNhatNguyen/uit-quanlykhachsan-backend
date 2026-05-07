# Import in dependency order so forward refs resolve correctly when model_rebuild() is called.

from src.models.hotel import Hotel, PopulatedHotel, CreateHotel, UpdateHotel
from src.models.room_type import RoomType, PopulatedRoomType, CreateRoomType, UpdateRoomType
from src.models.membership import Membership, PopulatedMembership, CreateMembership, UpdateMembership
from src.models.employee_account import EmployeeAccount, PopulatedEmployeeAccount, CreateEmployeeAccount, UpdateEmployeeAccount
from src.models.service import Service, PopulatedService, CreateService, UpdateService
from src.models.room import Room, PopulatedRoom, CreateRoom, UpdateRoom
from src.models.room_price_log import RoomPriceLog, PopulatedRoomPriceLog, CreateRoomPriceLog, UpdateRoomPriceLog
from src.models.service_price_log import ServicePriceLog, PopulatedServicePriceLog, CreateServicePriceLog, UpdateServicePriceLog
from src.models.customer import Customer, PopulatedCustomer, CreateCustomer, UpdateCustomer
from src.models.employee import Employee, PopulatedEmployee, Role, CreateEmployee, UpdateEmployee
from src.models.payment import Payment, PopulatedPayment, CreatePayment, UpdatePayment
from src.models.service_detail import ServicesDetail, PopulatedServicesDetail, CreateServicesDetail, UpdateServicesDetail
from src.models.booking_detail import BookingDetail, PopulatedBookingDetail, BookingStatus, CreateBookingDetail, UpdateBookingDetail
from src.models.booking import Booking, PopulatedBooking, CreateBooking, CreateBookingWithManyDetails, UpdateBooking, UpdateBookingWithManyDetails
from src.models.customer_history_purchase import CustomerHistoryPurchase, PopulatedCustomerHistoryPurchase, CreateCustomerHistoryPurchase, UpdateCustomerHistoryPurchase

# Resolve string forward references in Populated models
PopulatedHotel.model_rebuild(_types_namespace={"Room": Room})
PopulatedRoomType.model_rebuild(_types_namespace={"Room": Room})
PopulatedMembership.model_rebuild(_types_namespace={"Customer": Customer})
PopulatedEmployeeAccount.model_rebuild(_types_namespace={"Employee": Employee})
PopulatedRoom.model_rebuild(_types_namespace={"RoomPriceLog": RoomPriceLog})
PopulatedService.model_rebuild(_types_namespace={"ServicePriceLog": ServicePriceLog})
PopulatedPayment.model_rebuild(_types_namespace={"BookingDetail": BookingDetail})
PopulatedServicesDetail.model_rebuild(_types_namespace={"BookingDetail": BookingDetail})
PopulatedBookingDetail.model_rebuild(_types_namespace={"Booking": Booking})
