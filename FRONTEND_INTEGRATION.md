# Frontend Integration Guide — Hotel Booking API

> **Stack:** ReactJS + Axios  
> **Base URL:** `http://localhost:5001`  
> **All responses:** JSON. List endpoints return a paginated dict. Single-record endpoints return the object directly. Errors return `{ "detail": "..." }` (FastAPI standard) or `{ "error": "..." }` (DB-level error).

---

## 1. Axios Setup

Create `src/api/axios.js`:

```js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5001",
  headers: { "Content-Type": "application/json" },
});

// Optional: global error handler
api.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const message =
      err.response?.data?.detail ||
      err.response?.data?.error ||
      "Unknown error";
    return Promise.reject(new Error(message));
  }
);

export default api;
```

After this setup, every `api.get(...)` / `api.post(...)` call resolves directly to `response.data` — no need to call `.data` manually.

---

## 2. Pagination Response Shape

Every list endpoint (`GET /api/<resource>?page=1&page_size=10`) returns:

```json
{
  "page": 1,
  "page_size": 10,
  "total": 42,
  "total_pages": 5,
  "data": [ /* array of objects */ ]
}
```

**TypeScript / JSDoc type:**

```ts
interface PaginatedResponse<T> {
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
  data: T[];
}
```

---

## 3. Data Types

All field names match exactly what the API sends. `null` means the field is optional in the DB.

```ts
// Dates come as ISO strings: "2024-01-15" or "2024-01-15T14:30:00"

interface Booking {
  booking_id: number;
  customer_id: number;
  checkin_datetime: string | null;
  checkout_datetime: string | null;
  status: string | null;           // e.g. "confirmed", "checked_in", "checked_out"
  payment_id: number | null;
  hotel_id: number | null;
  created_at: string | null;
  notes: string | null;
}

interface BookingDetail {
  booking_detail_id: number;
  booking_id: number | null;
  room_id: number | null;
  quantity: number | null;
  price: number | null;
  amount: number | null;
}

interface Customer {
  customer_id: number;
  customer_name: string;
  sex: string;
  phone: string;
  email: string;
  birthday: string | null;         // "YYYY-MM-DD"
  membership_type_id: number;
  total_paid: number;
  notes: string | null;
  created_at: string | null;
  updated_at: string | null;
}

interface CustomerHistoryPurchase {
  id: number;
  customer_id: number | null;
  booking_id: number | null;
  booking_paid: number | null;
  cumulative_paid: number | null;
}

interface Counter {
  name: string;                    // PK is a string, not int
  value: number;
}

interface Employee {
  employee_id: number;
  employee_name: string | null;
  birthday: string | null;         // "YYYY-MM-DD"
  phone: string | null;
  is_working: string | null;       // e.g. "Y" / "N"
  position: string | null;
  start_working_date: string | null;
}

interface MembershipType {
  membership_type_id: number;
  membership_type_name: string | null;
  paid_from: number | null;
  paid_to: number | null;
}

interface Notification {
  id: number;
  title: string;
  sub: string | null;
  time_str: string | null;
  unread: boolean | null;
  icon: string | null;
}

interface Payment {
  payment_id: number;
  status: string | null;           // e.g. "pending", "paid"
}

interface PaymentDetail {
  payment_detail_id: number;
  cashier_id: number | null;
  payment_id: number | null;
  total_payment: number | null;
  payment_method: string | null;   // e.g. "cash", "card"
  payment_datetime: string | null; // ISO datetime
}

interface Room {
  room_id: number;
  room_number: string | null;
  room_type_id: number | null;
  price_per_night: number | null;
  capacity: string | null;
  room_area: string | null;
  is_smoking: boolean | null;
  description: string | null;
}

interface RoomInventory {
  room_id: number;
  room_number: string | null;
  room_type_id: number | null;
  is_available: number | null;     // 1 = available, 0 = occupied
  updated_at: string | null;
}

interface RoomInventoryLog {
  id: number;
  room_id: number | null;
  room_number: string | null;
  room_type_id: number | null;
  is_available: number | null;
  created_at: string | null;
}

interface RoomLogPrice {
  id: number;
  room_id: number | null;
  using_form_datetime: string | null;
  using_to_datetime: string | null;
  price_per_night: number | null;
}

interface RoomType {
  room_type_id: number;
  room_type_name: string | null;
}

interface ServiceDetail {
  service_detail: number;          // NOTE: PK field is named "service_detail", not "service_detail_id"
  booking_id: number | null;
  service_item_id: number | null;
  quantity: number | null;
  price: number | null;
  amount: number | null;
}

interface ServiceItem {
  service_item_id: number;
  service_item_name: string | null;
  catalog: string | null;
  price: number | null;
  used_count: number | null;
}
```

---

## 4. API Service Modules

Create one file per resource in `src/api/`. Each module exports typed functions.

### `src/api/bookings.js`

```js
import api from "./axios";

const BASE = "/api/bookings";

export const bookingsApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),

  get: (id) => api.get(`${BASE}/${id}`),

  create: (data) => api.post(BASE, data),
  // data shape: { customer_id, checkin_datetime, checkout_datetime, status, payment_id, hotel_id, notes }

  update: (id, data) => api.put(`${BASE}/${id}`, data),
  // Only send fields you want to change; the backend merges with existing values.

  delete: (id) => api.delete(`${BASE}/${id}`),
  // Returns the deleted Booking object.
};
```

### `src/api/bookingDetails.js`

```js
import api from "./axios";
const BASE = "/api/booking-details";

export const bookingDetailsApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),
  get: (id) => api.get(`${BASE}/${id}`),
  create: (data) => api.post(BASE, data),
  // data: { booking_id, room_id, quantity, price, amount }
  update: (id, data) => api.put(`${BASE}/${id}`, data),
  delete: (id) => api.delete(`${BASE}/${id}`),
};
```

### `src/api/customers.js`

```js
import api from "./axios";
const BASE = "/api/customers";

export const customersApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),
  get: (id) => api.get(`${BASE}/${id}`),
  create: (data) => api.post(BASE, data),
  // data: { customer_name, sex, phone, email, birthday, membership_type_id, total_paid }
  update: (id, data) => api.put(`${BASE}/${id}`, data),
  delete: (id) => api.delete(`${BASE}/${id}`),
};
```

### `src/api/customerHistoryPurchases.js`

```js
import api from "./axios";
const BASE = "/api/customer-history-purchases";

export const customerHistoryPurchasesApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),
  get: (id) => api.get(`${BASE}/${id}`),
  create: (data) => api.post(BASE, data),
  // data: { customer_id, booking_id, booking_paid, cumulative_paid }
  update: (id, data) => api.put(`${BASE}/${id}`, data),
  delete: (id) => api.delete(`${BASE}/${id}`),
};
```

### `src/api/employees.js`

```js
import api from "./axios";
const BASE = "/api/employees";

export const employeesApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),
  get: (id) => api.get(`${BASE}/${id}`),
  create: (data) => api.post(BASE, data),
  // data: { employee_name, birthday, phone, is_working, position, start_working_date }
  update: (id, data) => api.put(`${BASE}/${id}`, data),
  delete: (id) => api.delete(`${BASE}/${id}`),
};
```

### `src/api/membershipTypes.js`

```js
import api from "./axios";
const BASE = "/api/membership-types";

export const membershipTypesApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),
  get: (id) => api.get(`${BASE}/${id}`),
  create: (data) => api.post(BASE, data),
  // data: { membership_type_name, paid_from, paid_to }
  update: (id, data) => api.put(`${BASE}/${id}`, data),
  delete: (id) => api.delete(`${BASE}/${id}`),
};
```

### `src/api/notifications.js`

```js
import api from "./axios";
const BASE = "/api/notifications";

export const notificationsApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),
  get: (id) => api.get(`${BASE}/${id}`),
  create: (data) => api.post(BASE, data),
  // data: { title, sub, time_str, unread, icon }
  update: (id, data) => api.put(`${BASE}/${id}`, data),
  // To mark as read: update(id, { unread: false })
  delete: (id) => api.delete(`${BASE}/${id}`),
};
```

### `src/api/payments.js`

```js
import api from "./axios";
const BASE = "/api/payments";

export const paymentsApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),
  get: (id) => api.get(`${BASE}/${id}`),
  create: (data) => api.post(BASE, data),
  // data: { status }
  update: (id, data) => api.put(`${BASE}/${id}`, data),
  delete: (id) => api.delete(`${BASE}/${id}`),
};
```

### `src/api/paymentDetails.js`

```js
import api from "./axios";
const BASE = "/api/payment-details";

export const paymentDetailsApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),
  get: (id) => api.get(`${BASE}/${id}`),
  create: (data) => api.post(BASE, data),
  // data: { cashier_id, payment_id, total_payment, payment_method, payment_datetime }
  update: (id, data) => api.put(`${BASE}/${id}`, data),
  delete: (id) => api.delete(`${BASE}/${id}`),
};
```

### `src/api/rooms.js`

```js
import api from "./axios";
const BASE = "/api/rooms";

export const roomsApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),
  get: (id) => api.get(`${BASE}/${id}`),
  create: (data) => api.post(BASE, data),
  // data: { room_number, room_type_id, price_per_night, capacity, room_area, is_smoking, description }
  update: (id, data) => api.put(`${BASE}/${id}`, data),
  delete: (id) => api.delete(`${BASE}/${id}`),
};
```

### `src/api/roomInventories.js`

```js
import api from "./axios";
const BASE = "/api/room-inventories";

export const roomInventoriesApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),
  get: (roomId) => api.get(`${BASE}/${roomId}`),
  // PK is room_id (same as room)
  create: (data) => api.post(BASE, data),
  update: (roomId, data) => api.put(`${BASE}/${roomId}`, data),
  delete: (roomId) => api.delete(`${BASE}/${roomId}`),
};
```

### `src/api/roomInventoryLogs.js`

```js
import api from "./axios";
const BASE = "/api/room-inventory-logs";

export const roomInventoryLogsApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),
  get: (id) => api.get(`${BASE}/${id}`),
  create: (data) => api.post(BASE, data),
  update: (id, data) => api.put(`${BASE}/${id}`, data),
  delete: (id) => api.delete(`${BASE}/${id}`),
};
```

### `src/api/roomLogPrices.js`

```js
import api from "./axios";
const BASE = "/api/room-log-prices";

export const roomLogPricesApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),
  get: (id) => api.get(`${BASE}/${id}`),
  create: (data) => api.post(BASE, data),
  // data: { room_id, using_form_datetime, using_to_datetime, price_per_night }
  update: (id, data) => api.put(`${BASE}/${id}`, data),
  delete: (id) => api.delete(`${BASE}/${id}`),
};
```

### `src/api/roomTypes.js`

```js
import api from "./axios";
const BASE = "/api/room-types";

export const roomTypesApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),
  get: (id) => api.get(`${BASE}/${id}`),
  create: (data) => api.post(BASE, data),
  // data: { room_type_name }
  update: (id, data) => api.put(`${BASE}/${id}`, data),
  delete: (id) => api.delete(`${BASE}/${id}`),
};
```

### `src/api/serviceItems.js`

```js
import api from "./axios";
const BASE = "/api/service-items";

export const serviceItemsApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),
  get: (id) => api.get(`${BASE}/${id}`),
  create: (data) => api.post(BASE, data),
  // data: { service_item_name, catalog, price, used_count }
  update: (id, data) => api.put(`${BASE}/${id}`, data),
  delete: (id) => api.delete(`${BASE}/${id}`),
};
```

### `src/api/serviceDetails.js`

```js
import api from "./axios";
const BASE = "/api/service-details";

export const serviceDetailsApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),
  get: (id) => api.get(`${BASE}/${id}`),
  create: (data) => api.post(BASE, data),
  // data: { booking_id, service_item_id, quantity, price, amount }
  // NOTE: The PK field in the returned object is named "service_detail" (not "service_detail_id")
  update: (id, data) => api.put(`${BASE}/${id}`, data),
  delete: (id) => api.delete(`${BASE}/${id}`),
};
```

### `src/api/counters.js`

```js
import api from "./axios";
const BASE = "/api/counters";

export const countersApi = {
  list: (page = 1, pageSize = 10) =>
    api.get(BASE, { params: { page, page_size: pageSize } }),
  // PK is a string name, not a number
  get: (name) => api.get(`${BASE}/${name}`),
  create: (data) => api.post(BASE, data),
  // data: { name, value }
  update: (name, data) => api.put(`${BASE}/${name}`, data),
  delete: (name) => api.delete(`${BASE}/${name}`),
};
```

---

## 5. React Usage Examples

### List with pagination

```jsx
import { useState, useEffect } from "react";
import { bookingsApi } from "../api/bookings";

export function BookingList() {
  const [data, setData] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    bookingsApi
      .list(page, 10)
      .then((res) => {
        setData(res.data);
        setTotalPages(res.total_pages);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [page]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      {data.map((b) => (
        <div key={b.booking_id}>
          #{b.booking_id} — Customer {b.customer_id} — {b.status}
        </div>
      ))}
      <button disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>Prev</button>
      <span> Page {page} / {totalPages} </span>
      <button disabled={page >= totalPages} onClick={() => setPage((p) => p + 1)}>Next</button>
    </div>
  );
}
```

### Create

```jsx
import { bookingsApi } from "../api/bookings";

async function handleCreate() {
  try {
    const created = await bookingsApi.create({
      customer_id: 1,
      checkin_datetime: "2024-06-01T14:00:00",
      checkout_datetime: "2024-06-05T12:00:00",
      status: "confirmed",
      hotel_id: 1,
    });
    console.log("Created:", created); // full Booking object
  } catch (err) {
    console.error(err.message);
  }
}
```

### Partial update (only send changed fields)

```jsx
import { bookingsApi } from "../api/bookings";

// Only update status — other fields stay as-is (backend merges)
async function markCheckedIn(bookingId) {
  const updated = await bookingsApi.update(bookingId, { status: "checked_in" });
  console.log("Updated:", updated);
}
```

### Delete (returns deleted object)

```jsx
import { bookingsApi } from "../api/bookings";

async function handleDelete(bookingId) {
  const deleted = await bookingsApi.delete(bookingId);
  console.log("Deleted booking:", deleted); // the Booking that was removed
}
```

---

## 6. Error Handling

The axios interceptor in section 1 normalises errors so you always get a plain `Error` with a `.message` string. Wrap calls in `try/catch` or `.catch()`.

HTTP status codes the API returns:
- `200` — success
- `404` — record not found (message: `"<Resource> <id> not found"`)
- `422` — validation error (Pydantic, body shape wrong)
- `500` — database error (message from SQL Server driver)

---

## 7. Special Notes

| Resource | Special behaviour |
|---|---|
| **Counter** | PK `name` is a `string`. Use `countersApi.get("some_name")`, not a number. |
| **ServiceDetail** | The PK field in the returned JSON is `"service_detail"` (not `"service_detail_id"`). Use `item.service_detail` to get the ID. |
| **RoomInventory** | PK is `room_id` — shares the same ID space as Rooms. |
| **Notifications** | `unread` defaults to `true`. To mark read: `notificationsApi.update(id, { unread: false })`. |
| **Dates** | Send dates as ISO strings: `"YYYY-MM-DD"` for date-only fields, `"YYYY-MM-DDTHH:mm:ss"` for datetime fields. |
| **Update semantics** | You only need to send the fields you want to change. The backend always fetches the current record and merges, so omitted fields keep their existing values. |
| **Delete semantics** | All DELETE endpoints return the record that was deleted (not a boolean or empty body). |

---

## 8. API State Endpoint

```js
import api from "./axios";

// Returns system counters / state used by the admin dashboard
export const stateApi = {
  get: () => api.get("/api/state"),
  reset: () => api.post("/api/state/reset"),
};
```

---

## 9. Complete Endpoint Reference

| Resource | List | Get | Create | Update | Delete |
|---|---|---|---|---|---|
| State | `GET /api/state` | — | — | — | — |
| State Reset | — | — | `POST /api/state/reset` | — | — |
| Bookings | `GET /api/bookings` | `GET /api/bookings/:id` | `POST /api/bookings` | `PUT /api/bookings/:id` | `DELETE /api/bookings/:id` |
| Booking Details | `GET /api/booking-details` | `GET /api/booking-details/:id` | `POST /api/booking-details` | `PUT /api/booking-details/:id` | `DELETE /api/booking-details/:id` |
| Counters | `GET /api/counters` | `GET /api/counters/:name` | `POST /api/counters` | `PUT /api/counters/:name` | `DELETE /api/counters/:name` |
| Customers | `GET /api/customers` | `GET /api/customers/:id` | `POST /api/customers` | `PUT /api/customers/:id` | `DELETE /api/customers/:id` |
| Customer History | `GET /api/customer-history-purchases` | `GET /api/customer-history-purchases/:id` | `POST /api/customer-history-purchases` | `PUT /api/customer-history-purchases/:id` | `DELETE /api/customer-history-purchases/:id` |
| Employees | `GET /api/employees` | `GET /api/employees/:id` | `POST /api/employees` | `PUT /api/employees/:id` | `DELETE /api/employees/:id` |
| Membership Types | `GET /api/membership-types` | `GET /api/membership-types/:id` | `POST /api/membership-types` | `PUT /api/membership-types/:id` | `DELETE /api/membership-types/:id` |
| Notifications | `GET /api/notifications` | `GET /api/notifications/:id` | `POST /api/notifications` | `PUT /api/notifications/:id` | `DELETE /api/notifications/:id` |
| Payments | `GET /api/payments` | `GET /api/payments/:id` | `POST /api/payments` | `PUT /api/payments/:id` | `DELETE /api/payments/:id` |
| Payment Details | `GET /api/payment-details` | `GET /api/payment-details/:id` | `POST /api/payment-details` | `PUT /api/payment-details/:id` | `DELETE /api/payment-details/:id` |
| Rooms | `GET /api/rooms` | `GET /api/rooms/:id` | `POST /api/rooms` | `PUT /api/rooms/:id` | `DELETE /api/rooms/:id` |
| Room Inventories | `GET /api/room-inventories` | `GET /api/room-inventories/:room_id` | `POST /api/room-inventories` | `PUT /api/room-inventories/:room_id` | `DELETE /api/room-inventories/:room_id` |
| Room Inventory Logs | `GET /api/room-inventory-logs` | `GET /api/room-inventory-logs/:id` | `POST /api/room-inventory-logs` | `PUT /api/room-inventory-logs/:id` | `DELETE /api/room-inventory-logs/:id` |
| Room Log Prices | `GET /api/room-log-prices` | `GET /api/room-log-prices/:id` | `POST /api/room-log-prices` | `PUT /api/room-log-prices/:id` | `DELETE /api/room-log-prices/:id` |
| Room Types | `GET /api/room-types` | `GET /api/room-types/:id` | `POST /api/room-types` | `PUT /api/room-types/:id` | `DELETE /api/room-types/:id` |
| Service Details | `GET /api/service-details` | `GET /api/service-details/:id` | `POST /api/service-details` | `PUT /api/service-details/:id` | `DELETE /api/service-details/:id` |
| Service Items | `GET /api/service-items` | `GET /api/service-items/:id` | `POST /api/service-items` | `PUT /api/service-items/:id` | `DELETE /api/service-items/:id` |
