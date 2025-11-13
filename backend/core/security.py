"""Security utilities for password hashing and JWT token management."""

from datetime import datetime, timedelta
from typing import Optional

import hashlib
import bcrypt
from jose import JWTError, jwt

from core.config import settings


def hash_password(password: str) -> str:
    """Hash password using SHA-256 pre-hash + bcrypt.

    This avoids the bcrypt 72-byte input limitation by hashing the
    input with SHA-256 first, then passing the 32-byte digest to bcrypt.
    Returns the bcrypt hash as a UTF-8 string.
    """
    if isinstance(password, str):
        password = password.encode("utf-8")
    digest = hashlib.sha256(password).digest()
    hashed = bcrypt.hashpw(digest, bcrypt.gensalt())
    return hashed.decode("utf-8")


# Alias for compatibility
get_password_hash = hash_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a bcrypt hash produced by
    :func:`hash_password`.
    """
    if isinstance(plain_password, str):
        plain_password = plain_password.encode("utf-8")
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode("utf-8")
    digest = hashlib.sha256(plain_password).digest()
    try:
        return bcrypt.checkpw(digest, hashed_password)
    except ValueError:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT access token.

    Returns the token payload if valid, None otherwise.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None
