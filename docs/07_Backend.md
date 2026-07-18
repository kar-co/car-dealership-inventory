# Backend

Run migrations before the API: `..\\.venv\\Scripts\\python.exe -m alembic upgrade head` from `backend/fastapi_backend`. Start with `..\\.venv\\Scripts\\python.exe -m uvicorn app.main:app --reload`. Configure the PostgreSQL connection and JWT secret in `.env`.

For local frontend development, FastAPI should be available at `http://localhost:8000`, which is the Vite proxy target.
