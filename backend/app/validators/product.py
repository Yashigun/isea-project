from __future__ import annotations

import re
from decimal import Decimal


_SLUG_PATTERN = re.compile(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
)


_SHA256_PATTERN = re.compile(
    r"^[A-Fa-f0-9]{64}$"
)


_ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


def validate_product_name(
    value: str,
) -> str:
    """
    Validate product name.
    """

    value = " ".join(value.split())

    if not value:
        raise ValueError(
            "Product name cannot be empty."
        )

    if len(value) > 200:
        raise ValueError(
            "Product name cannot exceed 200 characters."
        )

    if any(not character.isprintable() for character in value):
        raise ValueError(
            "Product name contains invalid characters."
        )

    return value


def validate_slug(
    value: str,
) -> str:
    """
    Validate product/category slug.
    """

    value = value.strip().lower()

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


def validate_price(
    value: Decimal,
) -> Decimal:
    """
    Validate product price.
    """

    if value <= Decimal("0"):
        raise ValueError(
            "Price must be greater than zero."
        )

    return value.quantize(
        Decimal("0.01")
    )


def validate_discount_price(
    price: Decimal,
    discount_price: Decimal | None,
) -> Decimal | None:
    """
    Validate discount price.
    """

    if discount_price is None:
        return None

    if discount_price <= Decimal("0"):
        raise ValueError(
            "Discount price must be greater than zero."
        )

    if discount_price > price:
        raise ValueError(
            "Discount price cannot exceed product price."
        )

    return discount_price.quantize(
        Decimal("0.01")
    )


def validate_short_description(
    value: str | None,
) -> str | None:
    """
    Validate short description.
    """

    if value is None:
        return None

    value = " ".join(value.split())

    if len(value) > 200:
        raise ValueError(
            "Short description cannot exceed 200 characters."
        )

    return value


def validate_description(
    value: str | None,
) -> str | None:
    """
    Validate long description.
    """

    if value is None:
        return None

    value = value.strip()

    return value


def validate_original_filename(
    value: str,
) -> str:
    """
    Validate uploaded filename.
    """

    value = value.strip()

    if not value:
        raise ValueError(
            "Filename cannot be empty."
        )

    if len(value) > 255:
        raise ValueError(
            "Filename cannot exceed 255 characters."
        )

    if "/" in value or "\\" in value:
        raise ValueError(
            "Filename contains invalid characters."
        )

    return value


def validate_mime_type(
    value: str,
) -> str:
    """
    Validate uploaded MIME type.
    """

    if value not in _ALLOWED_MIME_TYPES:
        raise ValueError(
            "Unsupported image format."
        )

    return value


def validate_file_size(
    value: int,
    *,
    maximum_size: int = 10 * 1024 * 1024,
) -> int:
    """
    Validate uploaded image size.

    Default:
        10 MB
    """

    if value <= 0:
        raise ValueError(
            "Invalid file size."
        )

    if value > maximum_size:
        raise ValueError(
            "Uploaded file exceeds the maximum allowed size."
        )

    return value


def validate_sha256_hash(
    value: str,
) -> str:
    """
    Validate SHA-256 checksum.
    """

    value = value.lower()

    if not _SHA256_PATTERN.fullmatch(value):
        raise ValueError(
            "Invalid SHA-256 hash."
        )

    return value