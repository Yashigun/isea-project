from __future__ import annotations

from app.db.database import Base
from app.models.base import UUIDMixin, TimestampMixin

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Boolean

class Category(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "categories"
    
    __table_args__ = {
        "schema":"store"
    }
    
    name: Mapped[str] = mapped_column(
        String(100),
        unique = True,
        nullable = False
    )
    slug: Mapped[str] = mapped_column(
        String(150),
        nullable = False,
        unique = True,
        index = True
    )
    
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable = True
    ) 
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
    products: Mapped[list["Product"]] = relationship(
        back_populates="category"
    )