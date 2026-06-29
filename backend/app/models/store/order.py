from __future__ import annotations

import uuid
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    Enum as SQLEnum,
    ForeignKey,
    Numeric,
    String,
    Text,
    CheckConstraint
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.models.base import (
    UUIDMixin,
    TimestampMixin,
    PublicIdMixin,
)


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Order(
    Base,
    UUIDMixin,
    PublicIdMixin,
    TimestampMixin,
):
    __tablename__ = "orders"

    __table_args__ = (
        CheckConstraint(
            "subtotal >= 0",
            name="ck_order_subtotal_positive",
        ),
        CheckConstraint(
            "discount >= 0",
            name="ck_order_discount_positive",
        ),
        CheckConstraint(
            "shipping_cost >= 0",
            name="ck_order_shipping_cost_positive",
        ),
        CheckConstraint(
            "tax >= 0",
            name="ck_order_tax_positive",
        ),
        CheckConstraint(
            "total_amount >= 0",
            name="ck_order_total_positive",
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

    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False,
    )

    shipping_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    shipping_phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
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

    order_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    discount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=0,
        nullable=False,
    )

    shipping_cost: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=0,
        nullable=False,
    )

    tax: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=0,
        nullable=False,
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="orders",
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )

    payment: Mapped["Payment"] = relationship(
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan",
    )