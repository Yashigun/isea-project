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


class PhoneNumber(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "phone_numbers"

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

    phone_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="phone_numbers",
    )