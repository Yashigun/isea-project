from __future__ import annotations

import re


_POSTAL_CODE_PATTERN = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9\s-]{1,18}[A-Za-z0-9]$"
)


def _normalize(value: str, field_name: str) -> str:
    """
    Normalize text fields by removing
    leading/trailing whitespace and collapsing
    multiple spaces.
    """

    if value is None:
        raise ValueError(
            f"{field_name} is required."
        )

    value = " ".join(value.split())

    if not value:
        raise ValueError(
            f"{field_name} cannot be empty."
        )

    if any(not character.isprintable() for character in value):
        raise ValueError(
            f"{field_name} contains invalid characters."
        )

    return value


def validate_address_line(
    value: str,
) -> str:
    """
    Validate address line.
    """

    value = _normalize(
        value,
        "Address",
    )

    if len(value) > 255:
        raise ValueError(
            "Address cannot exceed 255 characters."
        )

    return value


def validate_city(
    value: str,
) -> str:
    """
    Validate city.
    """

    value = _normalize(
        value,
        "City",
    )

    if len(value) > 100:
        raise ValueError(
            "City cannot exceed 100 characters."
        )

    return value


def validate_state(
    value: str,
) -> str:
    """
    Validate state/province.
    """

    value = _normalize(
        value,
        "State",
    )

    if len(value) > 100:
        raise ValueError(
            "State cannot exceed 100 characters."
        )

    return value


def validate_country(
    value: str,
) -> str:
    """
    Validate country.
    """

    value = _normalize(
        value,
        "Country",
    )

    if len(value) > 100:
        raise ValueError(
            "Country cannot exceed 100 characters."
        )

    return value


def validate_postal_code(
    value: str,
) -> str:
    """
    Validate postal code.

    Supports international postal codes.
    """

    value = _normalize(
        value,
        "Postal code",
    )

    if len(value) > 20:
        raise ValueError(
            "Postal code cannot exceed 20 characters."
        )

    if not _POSTAL_CODE_PATTERN.fullmatch(value):
        raise ValueError(
            "Invalid postal code."
        )

    return value