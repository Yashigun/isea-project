from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.base import UUIDMixin, TimestampMixin, PublicIdMixin


class Cart(
    Base,
    UUIDMixin,
    TimestampMixin,
    PublicIdMixin
):
    __tablename__ = "carts"

    __table_args__ = {
        "schema": "store"
    }

    customer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "store.customers.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
        index=True,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="cart",
    )

    items: Mapped[list["CartItem"]] = relationship(
        back_populates="cart",
        cascade="all, delete-orphan",
    )