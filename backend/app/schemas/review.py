from __future__ import annotations

from pydantic import (
    Field,
    field_validator,
)

from app.schemas.common import (
    BaseRequestSchema,
    BaseResponseSchema,
)

from app.schemas.customer import (
    CustomerResponseSchema,
)

from app.validators.product import (
    validate_short_description,
    validate_description,
)


class ProductReviewCreateSchema(BaseRequestSchema):
    """
    Create a product review.
    """

    rating: int = Field(
        ge=1,
        le=5,
    )

    title: str = Field(
        min_length=2,
        max_length=150,
    )

    review: str = Field(
        min_length=2,
        max_length=5000,
    )

    age: str | None = Field(
        default=None,
        max_length=20,
    )

    @field_validator("title")
    @classmethod
    def validate_review_title(
        cls,
        value: str,
    ) -> str:
        return validate_short_description(value)

    @field_validator("review")
    @classmethod
    def validate_review(
        cls,
        value: str,
    ) -> str:
        validated = validate_description(value)

        if validated is None:
            raise ValueError(
                "Review cannot be empty."
            )

        return validated


class ProductReviewUpdateSchema(BaseRequestSchema):
    """
    Update a product review.
    """

    rating: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )

    title: str | None = Field(
        default=None,
        max_length=150,
    )

    review: str | None = Field(
        default=None,
        max_length=5000,
    )

    age: str | None = Field(
        default=None,
        max_length=20,
    )

    @field_validator("title")
    @classmethod
    def validate_review_title(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        return validate_short_description(value)

    @field_validator("review")
    @classmethod
    def validate_review(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        return validate_description(value)


class ProductReviewResponseSchema(BaseResponseSchema):
    """
    Product review returned by the API.
    """

    rating: int

    title: str

    review: str

    age: str | None = None

    customer: CustomerResponseSchema
