from __future__ import annotations

import uuid
from enum import Enum

from sqlalchemy import (
    Enum as SQLEnum,
    ForeignKey,
    Integer,
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
    PublicIdMixin
)


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


http_method_enum = SQLEnum(
    HttpMethod,
    name="http_method",
    values_callable=lambda enum: [m.value for m in enum],
)


class HttpProtocol(str, Enum):
    HTTP_1_1 = "HTTP/1.1"
    HTTP_2 = "HTTP/2"
    HTTP_3 = "HTTP/3"


http_protocol_enum = SQLEnum(
    HttpProtocol,
    name="http_protocol",
    values_callable=lambda enum: [m.value for m in enum],
)


class RequestSource(str, Enum):
    WEB = "web"
    MOBILE = "mobile"
    API = "api"


request_source_enum = SQLEnum(
    RequestSource,
    name="request_source",
    values_callable=lambda enum: [m.value for m in enum],
)


class RequestOutcome(str, Enum):
    SUCCESS = "success"
    REDIRECT = "redirect"
    CLIENT_ERROR = "client_error"
    SERVER_ERROR = "server_error"


request_outcome_enum = SQLEnum(
    RequestOutcome,
    name="request_outcome",
    values_callable=lambda enum: [m.value for m in enum],
)


class RequestLog(
    Base,
    UUIDMixin,
    TimestampMixin,
    PublicIdMixin
):
    __tablename__ = "request_logs"

    __table_args__ = {
        "schema": "security",
    }

    request_id: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
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

    method: Mapped[HttpMethod] = mapped_column(
        http_method_enum,
        nullable=False,
    )

    protocol: Mapped[HttpProtocol] = mapped_column(
        http_protocol_enum,
        nullable=False,
    )

    source: Mapped[RequestSource] = mapped_column(
        request_source_enum,
        nullable=False,
    )

    outcome: Mapped[RequestOutcome] = mapped_column(
        request_outcome_enum,
        nullable=False,
    )

    route: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    path: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
    )

    query_string: Mapped[str | None] = mapped_column(
        String(2048),
        nullable=True,
    )

    status_code: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    request_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    response_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    response_time_ms: Mapped[int] = mapped_column(
        Integer,
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

    referer: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="request_logs",
    )

    session: Mapped["CustomerSession"] = relationship(
        back_populates="request_logs",
    )