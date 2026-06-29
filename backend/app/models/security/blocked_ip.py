from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    String,
)
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.database import Base
from app.models.base import (
    UUIDMixin,
    TimestampMixin,
)


class BlockReason(str, Enum):
    BRUTE_FORCE = "brute_force"
    CREDENTIAL_STUFFING = "credential_stuffing"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    BOT = "bot"
    RATE_LIMIT = "rate_limit"
    MANUAL = "manual"
    OTHER = "other"


block_reason_enum = SQLEnum(
    BlockReason,
    name="block_reason",
    values_callable=lambda enum: [member.value for member in enum],
)


class BlockedIP(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "blocked_ips"

    __table_args__ = {
        "schema": "security",
    }

    ip_address: Mapped[str] = mapped_column(
        INET,
        nullable=False,
        unique=True,
        index=True,
    )

    reason: Mapped[BlockReason] = mapped_column(
        block_reason_enum,
        nullable=False,
    )

    blocked_by: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="system",
    )

    block_note: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    blocked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    permanently_blocked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )