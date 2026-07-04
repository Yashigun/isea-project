from __future__ import annotations

from typing import Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    SecretStr,
    field_validator,
)

from app.validators.customer import (
    normalize_email,
    validate_first_name,
    validate_last_name,
)

from app.validators.password import (
    validate_new_password,
    validate_password,
)




class RegisterRequestSchema(BaseModel):
    """
    Customer registration request.
    """

    first_name: str = Field(
        min_length=2,
        max_length=100,
    )

    last_name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    @field_validator("first_name")
    @classmethod
    def validate_first_name(
        cls,
        value: str,
    ) -> str:
        return validate_first_name(value)

    @field_validator("last_name")
    @classmethod
    def validate_last_name(
        cls,
        value: str,
    ) -> str:
        return validate_last_name(value)

    @field_validator("email")
    @classmethod
    def normalize_customer_email(
        cls,
        value: EmailStr,
    ) -> str:
        return normalize_email(str(value))

    @field_validator("password")
    @classmethod
    def validate_customer_password(
        cls,
        value: SecretStr,
    ) -> SecretStr:

        validate_password(
            value.get_secret_value(),
        )

        return value


class LoginRequestSchema(BaseModel):
    """
    Customer login request.
    """

    email: EmailStr

    password: SecretStr

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    @field_validator("email")
    @classmethod
    def normalize_customer_email(
        cls,
        value: EmailStr,
    ) -> str:
        return normalize_email(str(value))


class RefreshTokenRequestSchema(BaseModel):
    """
    Refresh an access token.
    """

    refresh_token: str = Field(
        min_length=32,
    )

    model_config = ConfigDict(
        extra="forbid",
    )


class LogoutRequestSchema(BaseModel):
    """
    Logout the current session.
    """

    refresh_token: str = Field(
        min_length=32,
    )

    model_config = ConfigDict(
        extra="forbid",
    )


class ChangePasswordRequestSchema(BaseModel):
    """
    Change customer password.
    """

    current_password: SecretStr

    new_password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )

    model_config = ConfigDict(
        extra="forbid",
    )

    @field_validator("current_password")
    @classmethod
    def validate_current_password(
        cls,
        value: SecretStr,
    ) -> SecretStr:

        validate_password(
            value.get_secret_value(),
        )

        return value

    @field_validator("new_password")
    @classmethod
    def validate_customer_new_password(
        cls,
        value: SecretStr,
        info,
    ) -> SecretStr:

        current_password = info.data.get(
            "current_password",
        )

        if current_password is not None:

            validate_new_password(
                current_password.get_secret_value(),
                value.get_secret_value(),
            )

        else:
            validate_password(
                value.get_secret_value(),
            )

        return value


class ForgotPasswordRequestSchema(BaseModel):
    """
    Request a password reset email.
    """

    email: EmailStr

    model_config = ConfigDict(
        extra="forbid",
    )

    @field_validator("email")
    @classmethod
    def normalize_customer_email(
        cls,
        value: EmailStr,
    ) -> str:
        return normalize_email(str(value))


class ResetPasswordRequestSchema(BaseModel):
    """
    Reset password using a reset token.
    """

    reset_token: str = Field(
        min_length=32,
    )

    new_password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )

    model_config = ConfigDict(
        extra="forbid",
    )

    @field_validator("new_password")
    @classmethod
    def validate_customer_password(
        cls,
        value: SecretStr,
    ) -> SecretStr:

        validate_password(
            value.get_secret_value(),
        )

        return value


class TokenResponseSchema(BaseModel):
    """
    Authentication response.
    """

    access_token: str

    refresh_token: str

    token_type: Literal["Bearer"] = "Bearer"

    expires_in: int = Field(
        gt=0,
        description="Access token lifetime in seconds.",
    )


class AuthenticatedCustomerSchema(BaseModel):
    """
    Authenticated customer information.
    """

    public_id: str

    first_name: str

    last_name: str

    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True,
    )
    
class AuthenticationResponseSchema(BaseModel):
    customer: AuthenticatedCustomerSchema
    tokens: TokenResponseSchema