# Security

Passwords are bcrypt hashes and are never stored in plaintext. JWTs expire according to `ACCESS_TOKEN_EXPIRE_MINUTES`; use a long random `SECRET_KEY` outside development. Keep `.env` secrets out of version control.

The signed `is_admin` claim controls frontend visibility only. Every protected and administrative request is independently checked by the API.
