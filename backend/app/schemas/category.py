from __future__ import annotations

from pydantic import (
    Field,
    field_validator,
)

from app.schemas.common import (
    BaseRequestSchema,
    BaseResponseSchema,
)

from app.validators.product import (
    validate_product_name,
    validate_slug,
)


class CategoryCreateSchema(BaseRequestSchema):
    """
    Create a category.
    """

    name: str = Field(
        min_length=2,
        max_length=100,
    )

    slug: str = Field(
        min_length=2,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    is_active: bool = True

    @field_validator("name")
    @classmethod
    def validate_category_name(
        cls,
        value: str,
    ) -> str:
        return validate_product_name(value)

    @field_validator("slug")
    @classmethod
    def validate_category_slug(
        cls,
        value: str,
    ) -> str:
        return validate_slug(value)


class CategoryUpdateSchema(BaseRequestSchema):
    """
    Update a category.
    """

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    slug: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    is_active: bool | None = None

    @field_validator("name")
    @classmethod
    def validate_category_name(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        return validate_product_name(value)

    @field_validator("slug")
    @classmethod
    def validate_category_slug(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        return validate_slug(value)


class CategoryResponseSchema(BaseResponseSchema):
    """
    Category returned by the API.
    """

    name: str

    slug: str

    description: str | None

    is_active: bool


class CategorySummarySchema(BaseResponseSchema):
    """
    Lightweight category schema used inside
    product responses.
    """

    name: str

    slug: str