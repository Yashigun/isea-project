from __future__ import annotations

from decimal import Decimal

from pydantic import (
    Field,
    field_validator,
)

from app.schemas.category import (
    CategorySummarySchema,
)
from app.schemas.common import (
    BaseRequestSchema,
    BaseResponseSchema,
)

from app.validators.product import (
    validate_description,
    validate_discount_price,
    validate_file_size,
    validate_mime_type,
    validate_original_filename,
    validate_price,
    validate_product_name,
    validate_sha256_hash,
    validate_short_description,
    validate_slug,
)


# --------------------------------------------------
# Product Image
# --------------------------------------------------


class ProductImageCreateSchema(BaseRequestSchema):
    """
    Create a product image.
    """

    original_filename: str

    mime_type: str

    file_size: int

    sha256_hash: str

    alt_text: str | None = Field(
        default=None,
        max_length=255,
    )

    display_order: int = Field(
        default=1,
        ge=1,
    )

    is_primary: bool = False

    @field_validator("original_filename")
    @classmethod
    def validate_filename(
        cls,
        value: str,
    ) -> str:
        return validate_original_filename(value)

    @field_validator("mime_type")
    @classmethod
    def validate_image_mime(
        cls,
        value: str,
    ) -> str:
        return validate_mime_type(value)

    @field_validator("file_size")
    @classmethod
    def validate_image_size(
        cls,
        value: int,
    ) -> int:
        return validate_file_size(value)

    @field_validator("sha256_hash")
    @classmethod
    def validate_image_hash(
        cls,
        value: str,
    ) -> str:
        return validate_sha256_hash(value)


class ProductImageResponseSchema(BaseResponseSchema):
    """
    Product image.
    """

    stored_filename: str

    original_filename: str

    mime_type: str

    file_size: int

    alt_text: str | None

    display_order: int

    is_primary: bool


# --------------------------------------------------
# Product
# --------------------------------------------------


class ProductCreateSchema(BaseRequestSchema):
    """
    Create a product.
    """

    category_public_id: str

    name: str = Field(
        min_length=2,
        max_length=200,
    )

    slug: str = Field(
        min_length=2,
        max_length=150,
    )

    short_description: str | None = Field(
        default=None,
        max_length=200,
    )

    description: str | None = None

    price: Decimal

    discount_price: Decimal | None = None

    is_active: bool = True

    @field_validator("name")
    @classmethod
    def validate_name(
        cls,
        value: str,
    ) -> str:
        return validate_product_name(value)

    @field_validator("slug")
    @classmethod
    def validate_product_slug(
        cls,
        value: str,
    ) -> str:
        return validate_slug(value)

    @field_validator("short_description")
    @classmethod
    def validate_short_desc(
        cls,
        value: str | None,
    ) -> str | None:
        return validate_short_description(value)

    @field_validator("description")
    @classmethod
    def validate_desc(
        cls,
        value: str | None,
    ) -> str | None:
        return validate_description(value)

    @field_validator("price")
    @classmethod
    def validate_product_price(
        cls,
        value: Decimal,
    ) -> Decimal:
        return validate_price(value)

    @field_validator("discount_price")
    @classmethod
    def validate_product_discount(
        cls,
        value: Decimal | None,
        info,
    ) -> Decimal | None:

        price = info.data.get("price")

        if price is None:
            return value

        return validate_discount_price(
            price,
            value,
        )


class ProductUpdateSchema(BaseRequestSchema):
    """
    Update a product.
    """

    category_public_id: str | None = None

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    slug: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    short_description: str | None = Field(
        default=None,
        max_length=200,
    )

    description: str | None = None

    price: Decimal | None = None

    discount_price: Decimal | None = None

    is_active: bool | None = None

    @field_validator("name")
    @classmethod
    def validate_name(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        return validate_product_name(value)

    @field_validator("slug")
    @classmethod
    def validate_slug_field(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        return validate_slug(value)

    @field_validator("short_description")
    @classmethod
    def validate_short_desc(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        return validate_short_description(value)

    @field_validator("description")
    @classmethod
    def validate_desc(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        return validate_description(value)

    @field_validator("price")
    @classmethod
    def validate_price_field(
        cls,
        value: Decimal | None,
    ) -> Decimal | None:

        if value is None:
            return value

        return validate_price(value)

    @field_validator("discount_price")
    @classmethod
    def validate_discount(
        cls,
        value: Decimal | None,
        info,
    ) -> Decimal | None:

        price = info.data.get("price")

        if value is None or price is None:
            return value

        return validate_discount_price(
            price,
            value,
        )


class ProductSummarySchema(BaseResponseSchema):
    """
    Lightweight product used in
    listings, search, wishlist and cart.
    """

    name: str

    slug: str

    price: Decimal

    discount_price: Decimal | None

    primary_image: str | None

    category: CategorySummarySchema


class ProductResponseSchema(ProductSummarySchema):
    """
    Complete product details.
    """

    short_description: str | None

    description: str | None

    is_active: bool

    images: list[ProductImageResponseSchema] = Field(
        default_factory=list,
    )