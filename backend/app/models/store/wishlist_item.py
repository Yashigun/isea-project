from __future__ import annotations

import uuid

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    UniqueConstraint
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.models.base import UUIDMixin, TimestampMixin, PublicIdMixin

class WishlistItem(Base, UUIDMixin, TimestampMixin, PublicIdMixin):
    __tablename__ = "wishlist_item"
    __table_args__ = (
        UniqueConstraint(
            "customer_id",
            "product_id",
            name="uq_customer_product_wishlist",
        ),
        {
            "schema": "store",
        },
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "store.customers.id",
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

    customer: Mapped["Customer"] = relationship(
        back_populates="wishlist_items",
    )

    product: Mapped["Product"] = relationship(
        back_populates="wishlist_items",
    )