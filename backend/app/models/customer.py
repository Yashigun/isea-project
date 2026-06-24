from datetime import datetime
from enum import Enum

from sqlalchemy import String, Integer, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.models.base import UUIDMixin, TimestampMixin

class AccountStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"

class Customer(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "customers"
    
    __table_args__ = {
        "schema":"store"
    }
    
    firstNmae: Mapped[str] = mapped_column(
        String(100),
        nullable = False
    )
    lasttNmae: Mapped[str] = mapped_column(
        String(100),
        nullable = False
    )
    
    email: Mapped[str] = mapped_column(
        String(255),
        unique = True,
        nullable = False,
        index = True
    )
    
    password_hash: Mapped[str]=  mapped_column(
        String(255),
        nullable = True
    )
    account_status: Mapped[AccountStatus] = mapped_column(
        SQLEnum(AccountStatus),
        default=AccountStatus.INACTIVE,
        nullable=False
    )

    failed_login_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    locked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )