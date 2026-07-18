# Car Dealership Inventory System

## Project overview

This assignment-scoped application manages dealership vehicle stock. The FastAPI backend provides JWT authentication, PostgreSQL persistence, vehicle management, price-aware search, purchasing, and restocking. The React frontend has exactly three views: Login, Register, and Dashboard.

## Tech stack

- FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT, and bcrypt
- Django administrative project
- React, Vite, HTML5, CSS3, and Tailwind CSS
- Pytest, Black, isort, and flake8

## Folder structure

```text
backend/fastapi_backend/   API application, migration, and tests
backend/django_backend/    Existing Django administrative project
frontend/                  React/Vite/Tailwind SPA
docs/                      Project and technical documentation
screenshots/               Final UI capture location
```

## Installation and database setup

Prerequisites: Python 3.13+, PostgreSQL, Node.js 18+ with npm, and the existing virtual environment. Create a PostgreSQL database named `car_dealership_db`, then configure `backend/fastapi_backend/.env`:

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=car_dealership_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
SECRET_KEY=replace-with-a-long-random-value
```

Apply migrations from `backend/fastapi_backend`:

```powershell
..\.venv\Scripts\python.exe -m alembic upgrade head
```

## Backend setup

```powershell
cd backend/fastapi_backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`; OpenAPI documentation is at `/docs`.

## Frontend setup

```powershell
cd frontend
Copy-Item .env.example .env
npm install
npm run dev
```

Vite proxies `/api` to `http://localhost:8000`. Set `VITE_API_BASE_URL` for another API origin. The signed JWT `is_admin` claim controls whether administrative buttons are shown; the API independently authorizes every administrative request.

## API list

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/api/auth/register` | Register an account |
| POST | `/api/auth/login` | Receive a JWT access token |
| GET | `/api/vehicles` | List vehicles (authenticated) |
| GET | `/api/vehicles/search` | Search text and/or `min_price` / `max_price` (authenticated) |
| POST | `/api/vehicles` | Add a vehicle (admin) |
| PUT | `/api/vehicles/{id}` | Update a vehicle (admin) |
| DELETE | `/api/vehicles/{id}` | Delete a vehicle (admin) |
| POST | `/api/vehicles/{id}/purchase` | Purchase stock (authenticated) |
| POST | `/api/vehicles/{id}/restock` | Restock stock (admin) |

## Testing and test report

```powershell
cd backend/fastapi_backend
..\.venv\Scripts\python.exe -m pytest app/tests -q
..\.venv\Scripts\python.exe -m black --check app alembic
..\.venv\Scripts\python.exe -m isort --check-only app alembic
..\.venv\Scripts\python.exe -m flake8 app alembic
```

| Check | Result |
| --- | --- |
| Backend API tests | 9 passed |
| PostgreSQL migration | `20260718_01 (head)` applied |
| Authentication, CRUD, search, purchase, restock | Covered by API tests |
| Black, isort, flake8 | Passed |
| Frontend dependency install | Passed (`npm install`) |
| Frontend production build | Passed (`npm run build`) |
| Frontend development server | Passed (Vite HTTP 200) |
| Frontend dependency audit | Follow-up required: Vite 5 development-server advisories need a major Vite 8 upgrade |

## Screenshots

The `screenshots/` directory is the destination for Login, Register, and Dashboard captures. The frontend runs successfully, but this environment has no usable browser surface for capture; add the final screenshots after opening the local app in a browser.

## My AI usage

AI assistance was used to analyse the CMA, implement assignment-scoped API and React/Tailwind changes, write tests, diagnose environment issues, and update documentation. I used it as a collaborative coding tool: requirements and test expectations were reviewed before code changes, and each generated change was verified with tests or builds. It accelerated boilerplate and diagnostics while the resulting behavior and known limitations were checked against the assignment. The user/assistant conversation record is in `PROMPTS.md`.

## Troubleshooting

- **`npm` is blocked by PowerShell policy:** run `npm.cmd install` or `npm.cmd run dev`.
- **Database connection fails:** confirm PostgreSQL is running, check `.env`, then run `alembic upgrade head`.
- **Admin buttons are absent:** the account must have `is_admin=true` in the database before login.
- **Search returns 422:** use non-negative numeric bounds and ensure `min_price` is not greater than `max_price`.
