# QShield — Changes & Setup Guide

## What Was Changed

### User Authentication System (New Feature)

A full user signup/login system was added to QShield with SQL Injection protection built in.

#### New Backend Files

| File | Purpose |
|---|---|
| `backend/app/db.py` | SQLAlchemy + SQLite database engine setup |
| `backend/app/models.py` | `User` table model (`id`, `email`, `hashed_password`) |
| `backend/app/schemas.py` | Pydantic validation schemas for request/response |
| `backend/app/core/security.py` | `bcrypt` password hashing + `pyjwt` JWT token generation |
| `backend/app/routers/auth.py` | `POST /auth/register` and `POST /auth/login` API endpoints |

#### Modified Backend Files

- **`backend/app/main.py`**
  - Imports reorganized to the top (removed mid-file imports)
  - Calls `Base.metadata.create_all()` on startup to auto-create the `qshield.db` SQLite database
  - Registered the `/auth` router

#### New Frontend Files

| File | Purpose |
|---|---|
| `frontend/src/context/AuthContext.jsx` | React context for storing the JWT and managing session state via `localStorage` |
| `frontend/src/components/ProtectedRoute.jsx` | Redirects unauthenticated users to `/login` |
| `frontend/src/pages/Login.jsx` | Login page (dark, Tailwind-styled) |
| `frontend/src/pages/Signup.jsx` | Signup page (auto-logs in after registration) |

#### Modified Frontend Files

- **`frontend/src/App.jsx`** — Wrapped the entire app in `<AuthProvider>`, moved all main pages behind `<ProtectedRoute>`, added `/login` and `/signup` public routes
- **`frontend/src/components/Sidebar.jsx`** — Added a **Logout** button at the bottom

---

### SQL Injection Protection

All database queries go through **SQLAlchemy ORM**, which uses parameterized queries exclusively. User input is never interpolated into raw SQL strings, making injection attacks impossible by design. Passwords are hashed with `bcrypt` before storage.

---

## How to Run

### Prerequisites

Install Python dependencies (run once):

```bash
pip install fastapi uvicorn sqlalchemy passlib bcrypt pyjwt python-multipart
```

Install frontend dependencies (run once, from `frontend/` directory):

```bash
cd frontend
npm install
```

---

### Running the Backend

From the `qshield-backend/` directory:

```bash
python -m uvicorn backend.app.main:app --reload
```

The API will be available at `http://localhost:8000`

- Swagger docs: `http://localhost:8000/docs`
- Auth endpoints: `http://localhost:8000/auth/register` and `http://localhost:8000/auth/login`

> A `qshield.db` SQLite file will be automatically created in `backend/app/` on first startup.

---

### Running the Frontend (Dev Mode)

From the `qshield-backend/frontend/` directory:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

> Make sure the backend is running first. The frontend calls `http://localhost:8000` for all API requests.

---

### Running Both Together (Production)

Build the frontend:

```bash
cd frontend
npm run build
```

Then start only the backend — it will automatically serve the built frontend from `frontend/dist/`:

```bash
cd ..
python -m uvicorn backend.app.main:app
```

Open `http://localhost:8000` in your browser.
