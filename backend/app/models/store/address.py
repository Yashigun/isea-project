from __future__ import annotations

import uuid

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class Address(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "customer_addresses"

    __table_args__ = {
        "schema": "store"
    }

    customer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "store.customers.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    address_line_1: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    address_line_2: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    postal_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="addresses",
    )