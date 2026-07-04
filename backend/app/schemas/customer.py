from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import Field

from pydantic import (
    EmailStr,
    Field,
    field_validator,
)

from app.schemas.common import (
    BaseRequestSchema,
    BaseResponseSchema,
)

from app.validators.customer import (
    normalize_email,
    validate_first_name,
    validate_last_name,
    validate_phone_number,
)


class CustomerUpdateSchema(BaseRequestSchema):
    """
    Update customer profile.
    """

    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    last_name: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    @field_validator( "first_name" )
    @classmethod
    def validate_first_name( cls, value: str | None) -> str | None:
        if value is None:
            return value

        return validate_first_name(value)
    
    @field_validator( "last_name" )
    @classmethod
    def validate_last_name(cls, value: str | None) -> str | None:
        if value is None or value.strip() == "":
            return None

        return validate_last_name(value)


class CustomerEmailUpdateSchema(BaseRequestSchema):
    """
    Change customer email.
    """

    email: EmailStr

    @field_validator("email")
    @classmethod
    def validate_email(
        cls,
        value: EmailStr,
    ) -> str:

        return normalize_email(
            str(value),
        )


class CustomerPhoneSchema(BaseRequestSchema):
    """
    Customer phone number.
    """

    phone_number: str

    is_default: bool = False

    @field_validator("phone_number")
    @classmethod
    def validate_phone(
        cls,
        value: str,
    ) -> str:

        return validate_phone_number(
            value,
        )


class CustomerAddressSummarySchema(BaseResponseSchema):
    """
    Customer address.
    """

    address_line_1: str

    address_line_2: str | None

    city: str

    state: str

    country: str

    postal_code: str

    is_default: bool


class CustomerPhoneResponseSchema(BaseResponseSchema):
    """
    Customer phone number.
    """

    phone_number: str

    is_default: bool


class CustomerResponseSchema(BaseResponseSchema):
    """
    Customer profile.
    """

    first_name: str

    last_name: str

    email: EmailStr

    account_status: str

    last_login_at: datetime | None


class CustomerProfileSchema(CustomerResponseSchema):
    """
    Complete customer profile.
    """
    phone_numbers: list[CustomerPhoneResponseSchema] = Field(
        default_factory=list,
    )

    addresses: list[CustomerAddressSummarySchema] = Field(
        default_factory=list,
    )