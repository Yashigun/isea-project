from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.models.base import TimestampMixin, UUIDMixin


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