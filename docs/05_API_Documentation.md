# API Documentation

Base path: `/api`. Errors use FastAPI's JSON `detail` field. Invalid requests return `422`; missing or invalid credentials return `401` or `403`; unknown vehicles return `404`; duplicate emails and insufficient stock return `409`.

| Method | Path | Access | Body |
| --- | --- | --- | --- |
| POST | `/auth/register` | Public | `email`, `password` |
| POST | `/auth/login` | Public | `email`, `password` |
| POST | `/vehicles` | Admin | vehicle fields |
| GET | `/vehicles` | Authenticated | — |
| GET | `/vehicles/search` | Authenticated | optional `query`, `min_price`, `max_price` |
| PUT | `/vehicles/{id}` | Admin | vehicle fields |
| DELETE | `/vehicles/{id}` | Admin | — |
| POST | `/vehicles/{id}/purchase` | Authenticated | positive `quantity` |
| POST | `/vehicles/{id}/restock` | Admin | positive `quantity` |

A vehicle contains `id`, `make`, `model`, `category`, positive two-decimal `price`, and non-negative `quantity`. Search combines supplied text and price filters; price bounds must be non-negative and `min_price` cannot exceed `max_price`. Send protected requests with `Authorization: Bearer <token>`.
