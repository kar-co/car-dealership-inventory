from datetime import datetime, timedelta, timezone

import bcrypt
from app.core.config import settings
from fastapi import HTTPException, status
from jose import JWTError, jwt

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def create_access_token(subject: str, is_admin: bool) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    return jwt.encode(
        {"sub": subject, "is_admin": is_admin, "exp": expires_at},
        settings.secret_key,
        settings.algorithm,
    )


def decode_access_token(token: str) -> str:
    try:
        subject = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        ).get("sub")
    except JWTError as error:
        raise credentials_exception from error
    if not subject:
        raise credentials_exception
    return subject
