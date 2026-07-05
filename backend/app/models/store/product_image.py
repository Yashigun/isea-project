from __future__ import annotations

import uuid

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    CheckConstraint,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.base import TimestampMixin, UUIDMixin, PublicIdMixin


class ProductImage(Base, UUIDMixin, TimestampMixin, PublicIdMixin):
    
    __tablename__ = "product_images"

    __table_args__ = (
        CheckConstraint(
            "file_size > 0",
            name="ck_product_image_file_size_positive",
        ),
        CheckConstraint(
            "display_order > 0",
            name="ck_product_image_display_order_positive",
        ),
        {
            "schema": "store",
        },
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "store.products.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # Required Cloudinary URL.
    url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    stored_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    sha256_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )

    alt_text: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    product: Mapped["Product"] = relationship(
        back_populates="images",
    )
