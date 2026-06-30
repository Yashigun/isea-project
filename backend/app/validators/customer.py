from __future__ import annotations

import re


_NAME_PATTERN = re.compile(
    r"^[A-Za-zÀ-ÿ]+(?:[ '-][A-Za-zÀ-ÿ]+)*$"
)


def validate_name(value: str) -> str:
    """
    Validate a customer's first or last name.

    Rules:
        - Required
        - 2-100 characters
        - Letters only
        - Spaces, apostrophes and hyphens allowed
        - Supports Latin accented characters
    """

    if value is None:
        raise ValueError(
            "Name is required."
        )

    value = " ".join(value.split())

    if not value:
        raise ValueError(
            "Name cannot be empty."
        )

    if len(value) < 2:
        raise ValueError(
            "Name must contain at least 2 characters."
        )

    if len(value) > 100:
        raise ValueError(
            "Name cannot exceed 100 characters."
        )

    if not _NAME_PATTERN.fullmatch(value):
        raise ValueError(
            "Name contains invalid characters."
        )

    return value


def validate_phone_number(value: str) -> str:
    """
    Validate a phone number.

    Rules:
        - Optional '+' prefix
        - Digits only
        - Length 7-15 digits (E.164)
    """

    if value is None:
        raise ValueError(
            "Phone number is required."
        )

    value = value.strip()

    if not value:
        raise ValueError(
            "Phone number cannot be empty."
        )

    normalized = (
        value.replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )

    if normalized.startswith("+"):
        digits = normalized[1:]
    else:
        digits = normalized

    if not digits.isdigit():
        raise ValueError(
            "Phone number must contain only digits."
        )

    if len(digits) < 7:
        raise ValueError(
            "Phone number is too short."
        )

    if len(digits) > 15:
        raise ValueError(
            "Phone number cannot exceed 15 digits."
        )

    return normalized


def normalize_email(email: str) -> str:
    """
    Normalize an email address before storage.

    Validation of the email format is handled
    by Pydantic's EmailStr.
    """

    if email is None:
        raise ValueError(
            "Email is required."
        )

    email = email.strip().lower()

    if not email:
        raise ValueError(
            "Email cannot be empty."
        )

    return email