from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.security.audit_log import AuditLog, AuditAction
from app.repositories.base import BaseRepository


class AuditLogRepository(BaseRepository[AuditLog]):
    """
    Repository responsible for audit log database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[AuditLog]:
        return AuditLog

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(self, audit_log_id: UUID) -> AuditLog | None:
        stmt = select(AuditLog).where(AuditLog.id == audit_log_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, public_id: str) -> AuditLog | None:
        stmt = select(AuditLog).where(AuditLog.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_customer_logs(self, customer_id: UUID, limit: int = 100) -> list[AuditLog]:
        stmt = (
            select(AuditLog)
            .where(AuditLog.customer_id == customer_id)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_action(self, action: AuditAction, limit: int = 100) -> list[AuditLog]:
        stmt = (
            select(AuditLog)
            .where(AuditLog.action == action)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_between(self, start_time: datetime, end_time: datetime) -> list[AuditLog]:
        stmt = (
            select(AuditLog)
            .where(AuditLog.created_at >= start_time)
            .where(AuditLog.created_at <= end_time)
            .order_by(AuditLog.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    async def count_logs(self) -> int:
        stmt = select(func.count(AuditLog.id))
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_customer_logs(self, customer_id: UUID) -> int:
        stmt = select(func.count(AuditLog.id)).where(AuditLog.customer_id == customer_id)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_action(self, action: AuditAction) -> int:
        stmt = select(func.count(AuditLog.id)).where(AuditLog.action == action)
        result = await self.db.execute(stmt)
        return result.scalar() or 0