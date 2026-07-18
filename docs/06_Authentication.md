# Authentication

Registration hashes passwords with bcrypt and stores only the hash. Login verifies the hash and issues a signed, expiring JWT containing the user subject and `is_admin` claim. All vehicle and inventory operations require a bearer token.

Administrative operations also require `users.is_admin` to be true in PostgreSQL. The frontend uses the signed claim only to display the relevant controls; FastAPI remains the authorization authority.
