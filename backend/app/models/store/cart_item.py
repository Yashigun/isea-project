from __future__ import annotations

import uuid

from sqlalchemy import (
    ForeignKey,
    Integer,
    UniqueConstraint,
    CheckConstraint
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.models.base import UUIDMixin, TimestampMixin, PublicIdMixin


class CartItem(
    Base,
    UUIDMixin,
    TimestampMixin,
    PublicIdMixin
):
    __tablename__ = "cart_items"

    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "product_id",
            name="uq_cart_product",
        ),
        CheckConstraint(
            "quantity > 0",
            name="ck_cart_item_quantity_positive",
        ),
        {
            "schema": "store",
        },
    )

    cart_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "store.carts.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "store.products.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        server_default="1",
    )

    cart: Mapped["Cart"] = relationship(
        back_populates="items",
    )

    product: Mapped["Product"] = relationship(
        back_populates="cart_items",
    )