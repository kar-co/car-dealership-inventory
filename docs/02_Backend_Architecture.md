# Backend Architecture

FastAPI routers handle HTTP requests, Pydantic schemas validate inputs and shape responses, SQLAlchemy models persist data, and dependencies provide database sessions and JWT authorization. Alembic owns schema evolution.

The React client consumes these routes through Vite's development `/api` proxy, keeping the completed backend API boundary unchanged.
