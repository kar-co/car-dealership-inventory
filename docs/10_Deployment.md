# Deployment

Set production PostgreSQL and JWT environment values, run `alembic upgrade head`, and serve `app.main:app` with a production ASGI process. Do not use the development default JWT secret in production.

Build the frontend with `npm run build` and serve its generated static assets. Set `VITE_API_BASE_URL` to the production API origin before building; the Vite development proxy is not used in production.
