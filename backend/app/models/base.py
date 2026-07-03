import uuid
from datetime import datetime
import secrets

from sqlalchemy import DateTime, func, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
import secrets
import string

ALPHABET = string.ascii_uppercase + string.digits

def generate_public_id(length: int = 16) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))

class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    server_onupdate=func.now(),
    nullable=False,
)
    
class PublicIdMixin:

    public_id: Mapped[str] = mapped_column(
        String(16),
        unique=True,
        nullable=False,
        index=True,
        default=generate_public_id,
    )