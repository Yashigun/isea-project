from __future__ import annotations

from pwdlib import PasswordHash

from app.security.jwt import (
    create_access_token,
    create_refresh_token,
)


refresh_token_hasher = PasswordHash.recommended()


def hash_refresh_token(
    refresh_token: str,
) -> str:
    """
    Hash a refresh token before storing it
    in the database.
    """

    return refresh_token_hasher.hash(refresh_token)


def verify_refresh_token_hash(
    refresh_token: str,
    hashed_refresh_token: str,
) -> bool:
    """
    Verify a refresh token against its
    stored Argon2 hash.
    """

    return refresh_token_hasher.verify(
        refresh_token,
        hashed_refresh_token,
    )


def refresh_token_needs_rehash(
    hashed_refresh_token: str,
) -> bool:
    """
    Determine whether the stored refresh
    token hash should be upgraded.
    """

    return refresh_token_hasher.check_needs_rehash(
        hashed_refresh_token,
    )


def rotate_refresh_token(
    subject: str,
) -> tuple[str, str]:
    """
    Generate a fresh access token and
    refresh token.

    Returns:
        (
            access_token,
            refresh_token,
        )
    """

    access_token = create_access_token(subject)
    refresh_token = create_refresh_token(subject)

    return (
        access_token,
        refresh_token,
    )