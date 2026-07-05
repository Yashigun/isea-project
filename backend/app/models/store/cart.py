from __future__ import annotations

import uuid
from decimal import Decimal

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

    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.items)

    @property
    def subtotal(self) -> Decimal:
        return sum((item.subtotal for item in self.items), Decimal("0.00"))

    @property
    def discount(self) -> Decimal:
        return Decimal("0.00")

    @property
    def tax(self) -> Decimal:
        return Decimal("0.00")

    @property
    def total_amount(self) -> Decimal:
        return self.subtotal + self.tax - self.discount
