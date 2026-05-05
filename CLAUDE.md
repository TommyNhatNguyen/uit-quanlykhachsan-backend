Tôi muốn dựng một trang quản trị về dịch vụ hotelbooking 
có những tính năng phù hợp với schema dml batabase postgres sau 
config database sqlserver
ip:165.22.106.126
port: 1433
db: master
user: sa
pass: Uit123@abc

-- ========================
-- DROP FOREIGN KEYS (nếu chạy lại)
-- ========================
IF OBJECT_ID('dbo.payment_detail', 'U') IS NOT NULL
BEGIN
    ALTER TABLE payment_detail DROP CONSTRAINT IF EXISTS fk_payment_detail_payment;
    ALTER TABLE payment_detail DROP CONSTRAINT IF EXISTS fk_payment_detail_cashier;
END
IF OBJECT_ID('dbo.customer_history_purchase', 'U') IS NOT NULL
BEGIN
    ALTER TABLE customer_history_purchase DROP CONSTRAINT IF EXISTS fk_chp_customer;
    ALTER TABLE customer_history_purchase DROP CONSTRAINT IF EXISTS fk_chp_booking;
END
IF OBJECT_ID('dbo.service_detail', 'U') IS NOT NULL
BEGIN
    ALTER TABLE service_detail DROP CONSTRAINT IF EXISTS fk_service_detail_booking;
    ALTER TABLE service_detail DROP CONSTRAINT IF EXISTS fk_service_detail_service_item;
END
IF OBJECT_ID('dbo.booking_detail', 'U') IS NOT NULL
BEGIN
    ALTER TABLE booking_detail DROP CONSTRAINT IF EXISTS fk_booking_detail_booking;
    ALTER TABLE booking_detail DROP CONSTRAINT IF EXISTS fk_booking_detail_room;
END
IF OBJECT_ID('dbo.booking', 'U') IS NOT NULL
BEGIN
    ALTER TABLE booking DROP CONSTRAINT IF EXISTS fk_booking_customer;
    ALTER TABLE booking DROP CONSTRAINT IF EXISTS fk_booking_payment;
END
IF OBJECT_ID('dbo.room_inventory_log', 'U') IS NOT NULL
    ALTER TABLE room_inventory_log DROP CONSTRAINT IF EXISTS fk_room_inventory_log_room;
IF OBJECT_ID('dbo.room_log_price', 'U') IS NOT NULL
    ALTER TABLE room_log_price DROP CONSTRAINT IF EXISTS fk_room_log_price_room;
IF OBJECT_ID('dbo.room', 'U') IS NOT NULL
BEGIN
    ALTER TABLE room DROP CONSTRAINT IF EXISTS fk_room_room_type;
    ALTER TABLE room DROP CONSTRAINT IF EXISTS fk_room_inventory;
END
IF OBJECT_ID('dbo.room_inventory', 'U') IS NOT NULL
    ALTER TABLE room_inventory DROP CONSTRAINT IF EXISTS fk_room_inventory_room_type;
IF OBJECT_ID('dbo.customer', 'U') IS NOT NULL
    ALTER TABLE customer DROP CONSTRAINT IF EXISTS fk_customer_membership;

-- ========================
-- DROP TABLES (nếu chạy lại)
-- ========================
DROP TABLE IF EXISTS dbo.payment_detail;
DROP TABLE IF EXISTS dbo.customer_history_purchase;
DROP TABLE IF EXISTS dbo.service_detail;
DROP TABLE IF EXISTS dbo.booking_detail;
DROP TABLE IF EXISTS dbo.booking;
DROP TABLE IF EXISTS dbo.room_log_price;
DROP TABLE IF EXISTS dbo.room_inventory_log;
DROP TABLE IF EXISTS dbo.room;
DROP TABLE IF EXISTS dbo.room_inventory;
DROP TABLE IF EXISTS dbo.customer;
DROP TABLE IF EXISTS dbo.service_item;
DROP TABLE IF EXISTS dbo.room_type;
DROP TABLE IF EXISTS dbo.employee;
DROP TABLE IF EXISTS dbo.payment;
DROP TABLE IF EXISTS dbo.membership_type;

-- ========================
-- INDEPENDENT TABLES
-- ========================
CREATE TABLE dbo.membership_type (
    membership_type_id   INT            PRIMARY KEY,
    membership_type_name NVARCHAR(255),
    paid_from            FLOAT,
    paid_to              FLOAT
);

CREATE TABLE dbo.payment (
    payment_id INT           PRIMARY KEY,
    status     NVARCHAR(255)
);

CREATE TABLE dbo.employee (
    employee_id        INT           PRIMARY KEY,
    employee_name      NVARCHAR(255),
    birthday           DATE,
    phone              NVARCHAR(50),
    is_working         NVARCHAR(50),
    position           NVARCHAR(100),
    start_working_date DATE
);

CREATE TABLE dbo.room_type (
    room_type_id   INT           PRIMARY KEY,
    room_type_name NVARCHAR(255)
);

CREATE TABLE dbo.service_item (
    service_item_id   INT           PRIMARY KEY,
    service_item_name NVARCHAR(255),
    catalog           NVARCHAR(255),
    price             FLOAT
);

-- ========================
-- DEPENDENT TABLES
-- ========================
CREATE TABLE dbo.customer (
    customer_id        INT           PRIMARY KEY,
    customer_name      NVARCHAR(255),
    sex                NVARCHAR(10),
    phone              NVARCHAR(50),
    email              NVARCHAR(255),
    birthday           DATE,
    membership_type_id INT,
    total_paid         FLOAT
);

CREATE TABLE dbo.room_inventory (
    room_id      INT        PRIMARY KEY,
    room_number  NVARCHAR(50),
    room_type_id INT,
    is_available FLOAT,
    updated_at   DATETIME2
);

CREATE TABLE dbo.room (
    room_id         INT           PRIMARY KEY,
    room_number     NVARCHAR(50),
    room_type_id    INT,
    price_per_night FLOAT,
    capacity        NVARCHAR(50),
    room_area       NVARCHAR(50),
    is_smoking      BIT,
    description     NVARCHAR(MAX)
);

CREATE TABLE dbo.room_log_price (
    id                  INT        PRIMARY KEY,
    room_id             INT,
    using_form_datetime DATETIME2,
    using_to_datetime   DATETIME2,
    price_per_night     FLOAT
);

CREATE TABLE dbo.room_inventory_log (
    id           INT        PRIMARY KEY,
    room_id      INT,
    room_number  NVARCHAR(50),
    room_type_id INT,
    is_available FLOAT,
    created_at   DATETIME2
);

CREATE TABLE dbo.booking (
    booking_id        INT           PRIMARY KEY,
    customer_id       INT,
    checkin_datetime  DATETIME2,
    checkout_datetime DATETIME2,
    status            NVARCHAR(100),
    payment_id        INT,
    hotel_id          INT,
    created_at        DATETIME2
);

CREATE TABLE dbo.booking_detail (
    booking_detail_id INT   PRIMARY KEY,
    booking_id        INT,
    room_id           INT,
    quantity          FLOAT,
    price             FLOAT,
    amount            FLOAT
);

CREATE TABLE dbo.service_detail (
    service_detail  INT   PRIMARY KEY,
    booking_id      INT,
    service_item_id INT,
    quantity        FLOAT,
    price           FLOAT,
    amount          FLOAT
);

CREATE TABLE dbo.customer_history_purchase (
    id              INT   PRIMARY KEY,
    customer_id     INT,
    booking_id      INT,
    booking_paid    FLOAT,
    cumulative_paid FLOAT
);

CREATE TABLE dbo.payment_detail (
    payment_detail_id INT           PRIMARY KEY,
    cashier_id        INT,
    payment_id        INT,
    total_payment     FLOAT,
    payment_method    NVARCHAR(100),
    payment_datetime  DATETIME2
);

-- ========================
-- FOREIGN KEYS
-- ========================
ALTER TABLE dbo.customer
    ADD CONSTRAINT fk_customer_membership
    FOREIGN KEY (membership_type_id) REFERENCES dbo.membership_type (membership_type_id);

ALTER TABLE dbo.room_inventory
    ADD CONSTRAINT fk_room_inventory_room_type
    FOREIGN KEY (room_type_id) REFERENCES dbo.room_type (room_type_id);

ALTER TABLE dbo.room
    ADD CONSTRAINT fk_room_room_type
    FOREIGN KEY (room_type_id) REFERENCES dbo.room_type (room_type_id);

ALTER TABLE dbo.room
    ADD CONSTRAINT fk_room_inventory
    FOREIGN KEY (room_id) REFERENCES dbo.room_inventory (room_id);

ALTER TABLE dbo.room_log_price
    ADD CONSTRAINT fk_room_log_price_room
    FOREIGN KEY (room_id) REFERENCES dbo.room (room_id);

ALTER TABLE dbo.room_inventory_log
    ADD CONSTRAINT fk_room_inventory_log_room
    FOREIGN KEY (room_id) REFERENCES dbo.room_inventory (room_id);

ALTER TABLE dbo.booking
    ADD CONSTRAINT fk_booking_customer
    FOREIGN KEY (customer_id) REFERENCES dbo.customer (customer_id);

ALTER TABLE dbo.booking
    ADD CONSTRAINT fk_booking_payment
    FOREIGN KEY (payment_id) REFERENCES dbo.payment (payment_id);

ALTER TABLE dbo.booking_detail
    ADD CONSTRAINT fk_booking_detail_booking
    FOREIGN KEY (booking_id) REFERENCES dbo.booking (booking_id);

ALTER TABLE dbo.booking_detail
    ADD CONSTRAINT fk_booking_detail_room
    FOREIGN KEY (room_id) REFERENCES dbo.room (room_id);

ALTER TABLE dbo.service_detail
    ADD CONSTRAINT fk_service_detail_booking
    FOREIGN KEY (booking_id) REFERENCES dbo.booking (booking_id);

ALTER TABLE dbo.service_detail
    ADD CONSTRAINT fk_service_detail_service_item
    FOREIGN KEY (service_item_id) REFERENCES dbo.service_item (service_item_id);

ALTER TABLE dbo.customer_history_purchase
    ADD CONSTRAINT fk_chp_customer
    FOREIGN KEY (customer_id) REFERENCES dbo.customer (customer_id);

ALTER TABLE dbo.customer_history_purchase
    ADD CONSTRAINT fk_chp_booking
    FOREIGN KEY (booking_id) REFERENCES dbo.booking (booking_id);

ALTER TABLE dbo.payment_detail
    ADD CONSTRAINT fk_payment_detail_payment
    FOREIGN KEY (payment_id) REFERENCES dbo.payment (payment_id);

ALTER TABLE dbo.payment_detail
    ADD CONSTRAINT fk_payment_detail_cashier
    FOREIGN KEY (cashier_id) REFERENCES dbo.employee (employee_id);