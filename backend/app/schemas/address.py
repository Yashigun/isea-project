from __future__ import annotations

from pydantic import (
    Field,
    field_validator,
)

from app.schemas.common import (
    BaseRequestSchema,
    BaseResponseSchema,
)

from app.validators.address import (
    validate_address_line,
    validate_city,
    validate_country,
    validate_postal_code,
    validate_state,
)


class AddressCreateSchema(BaseRequestSchema):
    """
    Create a customer address.
    """

    address_line_1: str = Field(
        max_length=255,
    )

    address_line_2: str | None = Field(
        default=None,
        max_length=255,
    )

    city: str = Field(
        max_length=100,
    )

    state: str = Field(
        max_length=100,
    )

    country: str = Field(
        max_length=100,
    )

    postal_code: str = Field(
        max_length=20,
    )

    is_default: bool = False

    @field_validator("address_line_1")
    @classmethod
    def validate_line_1(
        cls,
        value: str,
    ) -> str:
        return validate_address_line(value)

    @field_validator("address_line_2")
    @classmethod
    def validate_line_2(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        return validate_address_line(value)

    @field_validator("city")
    @classmethod
    def validate_customer_city(
        cls,
        value: str,
    ) -> str:
        return validate_city(value)

    @field_validator("state")
    @classmethod
    def validate_customer_state(
        cls,
        value: str,
    ) -> str:
        return validate_state(value)

    @field_validator("country")
    @classmethod
    def validate_customer_country(
        cls,
        value: str,
    ) -> str:
        return validate_country(value)

    @field_validator("postal_code")
    @classmethod
    def validate_customer_postal_code(
        cls,
        value: str,
    ) -> str:
        return validate_postal_code(value)


class AddressUpdateSchema(BaseRequestSchema):
    """
    Update a customer address.
    """

    address_line_1: str | None = Field(
        default=None,
        max_length=255,
    )

    address_line_2: str | None = Field(
        default=None,
        max_length=255,
    )

    city: str | None = Field(
        default=None,
        max_length=100,
    )

    state: str | None = Field(
        default=None,
        max_length=100,
    )

    country: str | None = Field(
        default=None,
        max_length=100,
    )

    postal_code: str | None = Field(
        default=None,
        max_length=20,
    )

    is_default: bool | None = None

    @field_validator(
        "address_line_1",
        "address_line_2",
    )
    @classmethod
    def validate_address_lines(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        return validate_address_line(value)

    @field_validator(
        "city",
    )
    @classmethod
    def validate_city_field(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        return validate_city(value)

    @field_validator(
        "state",
    )
    @classmethod
    def validate_state_field(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        return validate_state(value)

    @field_validator(
        "country",
    )
    @classmethod
    def validate_country_field(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        return validate_country(value)

    @field_validator(
        "postal_code",
    )
    @classmethod
    def validate_postal_code_field(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        return validate_postal_code(value)


class AddressResponseSchema(BaseResponseSchema):
    """
    Customer address returned by the API.
    """

    address_line_1: str

    address_line_2: str | None

    city: str

    state: str

    country: str

    postal_code: str

    is_default: bool