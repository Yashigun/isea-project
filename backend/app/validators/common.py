from __future__ import annotations

import re
import uuid


_SLUG_PATTERN = re.compile(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
)

_PUBLIC_ID_PATTERN = re.compile(
    r"^[A-Za-z0-9_-]{12,32}$"
)


def validate_uuid(value: str) -> str:
    """
    Validate that a string is a valid UUID.

    Returns:
        The original value.

    Raises:
        ValueError
    """

    try:
        uuid.UUID(value)

    except (ValueError, TypeError) as exc:
        raise ValueError(
            "Invalid UUID."
        ) from exc

    return value


def validate_slug(value: str) -> str:
    """
    Validate URL slug.

    Allowed:

    example-product

    gaming-laptop

    iphone-16-pro
    """

    value = value.strip()

    if not value:
        raise ValueError(
            "Slug cannot be empty."
        )

    if len(value) > 150:
        raise ValueError(
            "Slug cannot exceed 150 characters."
        )

    if not _SLUG_PATTERN.fullmatch(value):
        raise ValueError(
            "Slug contains invalid characters."
        )

    return value


def validate_public_id(value: str) -> str:
    """
    Validate public identifiers.
    """

    value = value.strip()

    if not _PUBLIC_ID_PATTERN.fullmatch(value):
        raise ValueError(
            "Invalid public identifier."
        )

    return value


def validate_page(
    page: int,
) -> int:
    """
    Validate pagination page number.
    """

    if page < 1:
        raise ValueError(
            "Page number must be at least 1."
        )

    return page


def validate_page_size(
    page_size: int,
    *,
    maximum: int = 100,
) -> int:
    """
    Validate pagination size.

    Limits maximum records returned
    in a single request.
    """

    if page_size < 1:
        raise ValueError(
            "Page size must be at least 1."
        )

    if page_size > maximum:
        raise ValueError(
            f"Page size cannot exceed {maximum}."
        )

    return page_size


def validate_sort_order(
    value: str,
) -> str:
    """
    Validate sorting direction.
    """

    value = value.lower().strip()

    if value not in {
        "asc",
        "desc",
    }:
        raise ValueError(
            "Sort order must be 'asc' or 'desc'."
        )

    return value