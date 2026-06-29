from __future__ import annotations

import uuid
from enum import Enum

from sqlalchemy import (
    Boolean,
    Enum as SQLEnum,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.models.base import (
    UUIDMixin,
    TimestampMixin,
)


class AttemptType(str, Enum):
    LOGIN = "login"
    REGISTER = "register"
    PASSWORD_RESET = "password_reset"
    EMAIL_VERIFICATION = "email_verification"
    REFRESH_TOKEN = "refresh_token"
    LOGOUT = "logout"


attempt_type_enum = SQLEnum(
    AttemptType,
    name="attempt_type",
    values_callable=lambda enum: [member.value for member in enum],
)


class AuthenticationFailureReason(str, Enum):
    INVALID_CREDENTIALS = "invalid_credentials"
    ACCOUNT_LOCKED = "account_locked"
    ACCOUNT_DISABLED = "account_disabled"
    EMAIL_NOT_VERIFIED = "email_not_verified"
    TOKEN_EXPIRED = "token_expired"
    TOKEN_REUSED = "token_reused"
    RATE_LIMITED = "rate_limited"
    UNKNOWN = "unknown"


authentication_failure_reason_enum = SQLEnum(
    AuthenticationFailureReason,
    name="authentication_failure_reason",
    values_callable=lambda enum: [member.value for member in enum],
)


class LoginAttempt(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "login_attempts"

    __table_args__ = {
        "schema": "security",
    }

    customer_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "store.customers.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    attempt_type: Mapped[AttemptType] = mapped_column(
        attempt_type_enum,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    ip_address: Mapped[str] = mapped_column(
        INET,
        nullable=False,
        index=True,
    )

    user_agent: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )

    successful: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    failure_reason: Mapped[AuthenticationFailureReason | None] = mapped_column(
        authentication_failure_reason_enum,
        nullable=True,
    )
    request_id: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        index=True,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="login_attempts",
    )