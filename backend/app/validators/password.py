from __future__ import annotations

from app.core.config import settings


def validate_password(
    password: str,
) -> str:
    """
    Validate password strength.

    Rules:
        - Minimum length from configuration
        - Maximum 128 characters
        - Cannot be empty
        - Cannot contain leading/trailing whitespace
        - Cannot contain control characters
        - Must not consist only of whitespace
    """

    if password is None:
        raise ValueError(
            "Password is required."
        )

    if password != password.strip():
        raise ValueError(
            "Password cannot begin or end with whitespace."
        )

    if len(password) < settings.PASSWORD_MIN_LENGTH:
        raise ValueError(
            f"Password must contain at least "
            f"{settings.PASSWORD_MIN_LENGTH} characters."
        )

    if len(password) > 128:
        raise ValueError(
            "Password cannot exceed 128 characters."
        )

    if password.isspace():
        raise ValueError(
            "Password cannot contain only whitespace."
        )

    for character in password:
        if character.isprintable() is False:
            raise ValueError(
                "Password contains invalid characters."
            )

    return password


def validate_new_password(
    current_password: str,
    new_password: str,
) -> str:
    """
    Validate a new password.

    Ensures the new password is valid and
    different from the current password.
    """

    validate_password(new_password)

    if current_password == new_password:
        raise ValueError(
            "New password must be different from the current password."
        )

    return new_password