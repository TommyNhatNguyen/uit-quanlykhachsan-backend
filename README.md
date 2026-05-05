# HotelBooking Admin — Backend

FastAPI backend connecting to SQL Server. Serves the admin UI at `/` and exposes a REST API at `/api/state`.

## Requirements

- Python 3.10+
- Access to SQL Server at `165.22.106.126:1433`

## Setup

**1. Create virtual environment**

```bash
python -m venv .venv
```

**2. Activate it**

- macOS / Linux:
  ```bash
  source .venv/bin/activate
  ```
- Windows (CMD):
  ```bat
  .venv\Scripts\activate.bat
  ```
- Windows (PowerShell):
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

## Run

```bash
fastapi dev app.py
```

The API will be available at `http://127.0.0.1:8000`.  
Interactive docs (Swagger UI) at `http://127.0.0.1:8000/docs`.

> To run on port 5001 instead, use:
> ```bash
> python app.py
> ```

## API

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/state` | Fetch all data (bookings, customers, rooms, …) |
| `PUT` | `/api/state` | Replace all data with the provided JSON body |
| `POST` | `/api/state/reset` | Delete all data |
