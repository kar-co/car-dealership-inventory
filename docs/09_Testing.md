# Testing

## Backend test suite

Run the API suite from `backend/fastapi_backend`:

```powershell
..\.venv\Scripts\python.exe -m pytest app/tests -q
```

The nine tests use an isolated SQLAlchemy database and cover registration, login, JWT claims, duplicate and invalid credentials, validation, protected reads, admin authorization, vehicle CRUD, text and price-range search, purchasing, oversell prevention, and restocking.

## Quality checks

```powershell
..\.venv\Scripts\python.exe -m black --check app alembic
..\.venv\Scripts\python.exe -m isort --check-only app alembic
..\.venv\Scripts\python.exe -m flake8 app alembic
```

All backend tests and checks passed during final verification. FastAPI emits dependency-inspection deprecation warnings under the project’s Python 3.14 runtime; they originate in the installed framework and do not fail the tests.

## Frontend verification

`npm install`, `npm run build`, and a live Vite development-server request all passed during final verification. Verify Login, Register, Dashboard loading/error states, server-backed search, category filtering, disabled sold-out purchases, and admin controls against the running API in a browser.

`npm audit` reports development-server advisories in Vite 5. The compatible major Vite 8 upgrade did not complete in this environment before command timeout, so it remains a dependency-maintenance follow-up rather than an application functional failure.
