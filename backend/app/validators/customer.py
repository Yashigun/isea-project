from __future__ import annotations

import re
from typing import Optional


_NAME_PATTERN = re.compile(
    r"^[A-Za-zÀ-ÿ]+(?:[ '-][A-Za-zÀ-ÿ]+)*$"
)



def validate_name(
    value: str,
    *,
    field_name: str = "Name",
    min_length: int = 2,
    max_length: int = 150,
) -> str:
    """
    Validate product/category names.

    Rules:
        - Required
        - 2-150 characters (configurable)
        - Letters and numbers allowed
        - Supports accented characters
        - Allows common commerce punctuation:
            - '
            - -
            - &
            - .
            - ,
            - (
            - )
            - /
            - +
            - %
        - Consecutive spaces are normalized
    """

    if value is None:
        raise ValueError(f"{field_name} is required.")

    value = " ".join(value.split())

    if not value:
        raise ValueError(f"{field_name} cannot be empty.")

    if len(value) < min_length:
        raise ValueError(
            f"{field_name} must contain at least {min_length} characters."
        )

    if len(value) > max_length:
        raise ValueError(
            f"{field_name} cannot exceed {max_length} characters."
        )

    if not _NAME_PATTERN.fullmatch(value):
        raise ValueError(
            f"{field_name} contains invalid characters."
        )

    return value

def validate_first_name(value: str) -> str:
    """
    Validate a customer's first name.

    Rules:
        - Required
        - 2-100 characters
        - Letters only
        - Spaces, apostrophes and hyphens allowed
        - Supports Latin accented characters
    """

    if value is None:
        raise ValueError("First name is required.")

    value = " ".join(value.split())

    if not value:
        raise ValueError("First name cannot be empty.")

    if len(value) < 2:
        raise ValueError("First name must contain at least 2 characters.")

    if len(value) > 100:
        raise ValueError("First name cannot exceed 100 characters.")

    if not _NAME_PATTERN.fullmatch(value):
        raise ValueError("First name contains invalid characters.")

    return value


def validate_last_name(value: Optional[str]) -> Optional[str]:
    """
    Validate a customer's last name.

    Rules:
        - Optional
        - If provided, 2-100 characters
        - Letters only
        - Spaces, apostrophes and hyphens allowed
        - Supports Latin accented characters
    """

    # Optional field
    if value is None:
        return None

    value = " ".join(value.split())

    # Treat empty or whitespace-only input as no last name
    if value == "":
        return None

    if len(value) < 2:
        raise ValueError("Last name must contain at least 2 characters.")

    if len(value) > 100:
        raise ValueError("Last name cannot exceed 100 characters.")

    if not _NAME_PATTERN.fullmatch(value):
        raise ValueError("Last name contains invalid characters.")

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
        raise ValueError("Phone number is required.")

    value = value.strip()

    if not value:
        raise ValueError("Phone number cannot be empty.")

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
        raise ValueError("Phone number must contain only digits.")

    if len(digits) < 7:
        raise ValueError("Phone number is too short.")

    if len(digits) > 15:
        raise ValueError("Phone number cannot exceed 15 digits.")

    return normalized


def normalize_email(email: str) -> str:
    """
    Normalize an email address before storage.

    Validation of the email format is handled
    by Pydantic's EmailStr.
    """

    if email is None:
        raise ValueError("Email is required.")

    email = email.strip().lower()

    if not email:
        raise ValueError("Email cannot be empty.")

    return email