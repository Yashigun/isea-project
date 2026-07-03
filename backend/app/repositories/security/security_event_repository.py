from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.security.security_event import SecurityEvent, EventSeverity, SecurityEventType
from app.repositories.base import BaseRepository


class SecurityEventRepository(BaseRepository[SecurityEvent]):
    """
    Repository responsible for security event database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[SecurityEvent]:
        return SecurityEvent

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(self, event_id: UUID) -> SecurityEvent | None:
        stmt = select(SecurityEvent).where(SecurityEvent.id == event_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, public_id: str) -> SecurityEvent | None:
        stmt = select(SecurityEvent).where(SecurityEvent.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_customer_events(self, customer_id: UUID, limit: int = 100) -> list[SecurityEvent]:
        stmt = (
            select(SecurityEvent)
            .where(SecurityEvent.customer_id == customer_id)
            .order_by(SecurityEvent.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_ip(self, ip_address: str, limit: int = 100) -> list[SecurityEvent]:
        stmt = (
            select(SecurityEvent)
            .where(SecurityEvent.ip_address == ip_address)
            .order_by(SecurityEvent.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_type(self, event_type: SecurityEventType, limit: int = 100) -> list[SecurityEvent]:
        stmt = (
            select(SecurityEvent)
            .where(SecurityEvent.event_type == event_type)
            .order_by(SecurityEvent.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_severity(self, severity: EventSeverity, limit: int = 100) -> list[SecurityEvent]:
        stmt = (
            select(SecurityEvent)
            .where(SecurityEvent.severity == severity)
            .order_by(SecurityEvent.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_between(self, start_time: datetime, end_time: datetime) -> list[SecurityEvent]:
        stmt = (
            select(SecurityEvent)
            .where(SecurityEvent.created_at >= start_time)
            .where(SecurityEvent.created_at <= end_time)
            .order_by(SecurityEvent.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    async def count_events(self) -> int:
        stmt = select(func.count(SecurityEvent.id))
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_by_type(self, event_type: SecurityEventType) -> int:
        stmt = select(func.count(SecurityEvent.id)).where(SecurityEvent.event_type == event_type)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_by_severity(self, severity: EventSeverity) -> int:
        stmt = select(func.count(SecurityEvent.id)).where(SecurityEvent.severity == severity)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_ip_events(self, ip_address: str, since: datetime) -> int:
        stmt = (
            select(func.count(SecurityEvent.id))
            .where(SecurityEvent.ip_address == ip_address)
            .where(SecurityEvent.created_at >= since)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0