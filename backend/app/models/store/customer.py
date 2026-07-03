from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.base import TimestampMixin, UUIDMixin

from typing import Optional


class AccountStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"


account_status_enum = SQLEnum(
    AccountStatus,
    name="account_status",
    values_callable=lambda enum: [member.value for member in enum],
)
class AuthProvider(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"


class Customer(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "customers"

    __table_args__ = {
        "schema": "store"
    }

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    password_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    account_status: Mapped[AccountStatus] = mapped_column(
        account_status_enum,
        default=AccountStatus.INACTIVE,
        nullable=False
    )

    failed_login_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    locked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    auth_provider: Mapped[AuthProvider] = mapped_column(
        SQLEnum(AuthProvider), default=AuthProvider.EMAIL, nullable=False
    )
    google_id: Mapped[Optional[str]] = mapped_column(
        String(255), unique=True, nullable=True, index=True
    )
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_admin: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, index=True
    )
    addresses: Mapped[list["Address"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
    )
    phone_numbers: Mapped[list["PhoneNumber"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
    )
    wishlist_items: Mapped[list["WishlistItem"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
    )
    cart: Mapped["Cart"] = relationship(
        back_populates="customer",
        uselist=False,
        cascade="all, delete-orphan",
    )
    orders: Mapped[list["Order"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
    )
    reviews: Mapped[list["ProductReview"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
    )
    sessions: Mapped[list["CustomerSession"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
    )
    login_attempts: Mapped[list["LoginAttempt"]] = relationship(
        back_populates="customer",
    )
    request_logs: Mapped[list["RequestLog"]] = relationship(
        back_populates="customer",
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        back_populates="customer",
    )
    security_events: Mapped[list["SecurityEvent"]] = relationship(
        back_populates="customer",
    )