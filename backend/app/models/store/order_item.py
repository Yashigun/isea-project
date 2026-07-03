from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.models.base import UUIDMixin, TimestampMixin, PublicIdMixin


class OrderItem(
    Base,
    UUIDMixin,
    TimestampMixin,
    PublicIdMixin
):
    __tablename__ = "order_items"

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="ck_order_item_quantity_positive",
        ),
        CheckConstraint(
            "unit_price > 0",
            name="ck_order_item_unit_price_positive",
        ),
        CheckConstraint(
            "subtotal >= 0",
            name="ck_order_item_subtotal_positive",
        ),
        {
            "schema": "store",
        },
    )

    order_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "store.orders.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "store.products.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    product_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    order: Mapped["Order"] = relationship(
        back_populates="items",
    )

    product: Mapped["Product"] = relationship(
        back_populates="order_items",
    )