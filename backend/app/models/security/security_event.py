from __future__ import annotations

import uuid
from enum import Enum

from sqlalchemy import (
    Boolean,
    Enum as SQLEnum,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import (
    INET,
    JSONB,
)
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


class EventSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


event_severity_enum = SQLEnum(
    EventSeverity,
    name="event_severity",
    values_callable=lambda enum: [member.value for member in enum],
)


class SecurityEventType(str, Enum):
    BRUTE_FORCE = "brute_force"
    CREDENTIAL_STUFFING = "credential_stuffing"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    CSRF = "csrf"
    PATH_TRAVERSAL = "path_traversal"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    TOKEN_REUSE = "token_reuse"
    INVALID_TOKEN = "invalid_token"
    SUSPICIOUS_LOGIN = "suspicious_login"
    BOT_DETECTED = "bot_detected"
    ACCOUNT_LOCKED = "account_locked"
    UNKNOWN = "unknown"


security_event_type_enum = SQLEnum(
    SecurityEventType,
    name="security_event_type",
    values_callable=lambda enum: [member.value for member in enum],
)


class SecurityEvent(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "security_events"

    __table_args__ = {
        "schema": "security",
    }

    request_id: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        index=True,
    )

    customer_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "store.customers.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    session_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "security.customer_sessions.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    event_type: Mapped[SecurityEventType] = mapped_column(
        security_event_type_enum,
        nullable=False,
    )

    severity: Mapped[EventSeverity] = mapped_column(
        event_severity_enum,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    ip_address: Mapped[str] = mapped_column(
        INET,
        nullable=False,
        index=True,
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    evidence: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    resolved: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="security_events",
    )

    session: Mapped["CustomerSession"] = relationship(
        back_populates="security_events",
    )