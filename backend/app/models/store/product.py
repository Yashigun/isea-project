from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.db.database import Base
from app.models.base import TimestampMixin, UUIDMixin, PublicIdMixin


class Product(Base, UUIDMixin, TimestampMixin, PublicIdMixin):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint(
            "price > 0",
            name="ck_product_price_positive",
        ),
        CheckConstraint(
            "discount_price IS NULL OR discount_price <= price",
            name="ck_product_discount_price",
        ),
        {
            "schema": "store",
        },
    )

    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("store.categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True
    )

    slug: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
    )

    short_description: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    discount_price: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    category: Mapped["Category"] = relationship(
        back_populates="products",
    )
    
    images: Mapped[list["ProductImage"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        order_by="ProductImage.display_order",
    )
    wishlist_items: Mapped[list["WishlistItem"]] = relationship(
        back_populates="product",
    )
    cart_items: Mapped[list["CartItem"]] = relationship(
        back_populates="product",
    )
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="product",
    )
    reviews: Mapped[list["ProductReview"]] = relationship(
        back_populates="product",
    )
    
    @hybrid_property
    def primary_image(self) -> str | None:
        if self.images:
            # Get the first image marked as primary, or the first image
            primary = next((img for img in self.images if img.is_primary), None)
            return primary.url if primary else self.images[0].url
        return None