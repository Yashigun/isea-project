from __future__ import annotations

import uuid
from enum import Enum

from sqlalchemy import (
    Enum as SQLEnum,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import (
    INET,
    JSONB,
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
    PublicIdMixin
)


class AuditAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

    LOGIN = "login"
    LOGOUT = "logout"

    PASSWORD_CHANGE = "password_change"
    EMAIL_CHANGE = "email_change"

    ADDRESS_CHANGE = "address_change"
    PHONE_NUMBER_CHANGE = "phone_number_change"

    ORDER_PLACED = "order_placed"
    ORDER_CANCELLED = "order_cancelled"

    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILED = "payment_failed"


audit_action_enum = SQLEnum(
    AuditAction,
    name="audit_action",
    values_callable=lambda enum: [member.value for member in enum],
)


class EntityType(str, Enum):
    CUSTOMER = "customer"
    PRODUCT = "product"
    CATEGORY = "category"
    ORDER = "order"
    PAYMENT = "payment"
    ADDRESS = "address"
    PHONE_NUMBER = "phone_number"
    REVIEW = "review"
    CART = "cart"
    WISHLIST = "wishlist"


entity_type_enum = SQLEnum(
    EntityType,
    name="entity_type",
    values_callable=lambda enum: [member.value for member in enum],
)


class AuditLog(
    Base,
    UUIDMixin,
    TimestampMixin,
    PublicIdMixin
):
    __tablename__ = "audit_logs"

    __table_args__ = {
        "schema": "security",
    }

    request_id: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )

    customer_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "store.customers.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    action: Mapped[AuditAction] = mapped_column(
        audit_action_enum,
        nullable=False,
    )

    entity_type: Mapped[EntityType] = mapped_column(
        entity_type_enum,
        nullable=False,
    )
    entity_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    entity_public_id: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
        index=True,
    )

    old_data: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    new_data: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    ip_address: Mapped[str] = mapped_column(
        INET,
        nullable=False,
        index=True,
    )

    user_agent: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="audit_logs",
    )