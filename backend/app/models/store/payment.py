from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
import uuid

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Numeric,
    String,
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


class PaymentMethod(str, Enum):
    CARD = "card"
    UPI = "upi"
    NET_BANKING = "net_banking"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class Payment(
    Base,
    UUIDMixin,
    PublicIdMixin,
    TimestampMixin,
):
    __tablename__ = "payments"

    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="ck_payment_amount_positive",
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
        unique=True,
        nullable=False,
        index=True,
    )

    payment_method: Mapped[PaymentMethod] = mapped_column(
        SQLEnum(PaymentMethod),
        nullable=False,
    )

    payment_status: Mapped[PaymentStatus] = mapped_column(
        SQLEnum(PaymentStatus),
        default=PaymentStatus.PENDING,
        nullable=False,
    )

    gateway_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    transaction_reference: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    order: Mapped["Order"] = relationship(
        back_populates="payment",
    )