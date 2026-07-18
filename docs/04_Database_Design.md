# Database Design

`users` stores `id`, unique `email`, `password_hash`, and the required `is_admin` authorization flag. `vehicles` stores `id`, `make`, `model`, `category`, decimal `price`, and non-negative `quantity`. The initial Alembic revision creates both tables and lookup indexes.

The frontend never stores vehicle data as a separate source of truth; it reloads data from the API after purchases and administration changes.
