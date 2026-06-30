from __future__ import annotations

import uuid
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from enum import Enum
from typing import Any

from jose import jwt
from jose.exceptions import (
    ExpiredSignatureError,
    JWTClaimsError,
    JWTError,
)

from app.core.config import settings


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


def _create_token(
    subject: str,
    token_type: TokenType,
    secret_key: str,
    expires_delta: timedelta,
) -> str:
    """
    Internal helper to create a signed JWT.
    """

    now = datetime.now(timezone.utc)

    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type.value,
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": now + expires_delta,
    }

    return jwt.encode(
        claims=payload,
        key=secret_key,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_access_token(
    subject: str,
) -> str:
    """
    Create a signed access token.
    """

    return _create_token(
        subject=subject,
        token_type=TokenType.ACCESS,
        secret_key=settings.JWT_ACCESS_SECRET_KEY,
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        ),
    )


def create_refresh_token(
    subject: str,
) -> str:
    """
    Create a signed refresh token.
    """

    return _create_token(
        subject=subject,
        token_type=TokenType.REFRESH,
        secret_key=settings.JWT_REFRESH_SECRET_KEY,
        expires_delta=timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
        ),
    )


def decode_token(
    token: str,
    secret_key: str,
) -> dict[str, Any]:
    """
    Decode and validate a JWT.

    Raises:
        ExpiredSignatureError
        JWTClaimsError
        JWTError
    """

    return jwt.decode(
        token=token,
        key=secret_key,
        algorithms=[settings.JWT_ALGORITHM],
        issuer=settings.JWT_ISSUER,
        audience=settings.JWT_AUDIENCE,
    )


def verify_access_token(
    token: str,
) -> dict[str, Any]:
    """
    Decode and verify an access token.
    """

    payload = decode_token(
        token=token,
        secret_key=settings.JWT_ACCESS_SECRET_KEY,
    )

    if payload.get("type") != TokenType.ACCESS.value:
        raise JWTClaimsError("Invalid token type.")

    return payload


def verify_refresh_token(
    token: str,
) -> dict[str, Any]:
    """
    Decode and verify a refresh token.
    """

    payload = decode_token(
        token=token,
        secret_key=settings.JWT_REFRESH_SECRET_KEY,
    )

    if payload.get("type") != TokenType.REFRESH.value:
        raise JWTClaimsError("Invalid token type.")

    return payload