from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.security.audit_log import AuditLog
from app.repositories.base import BaseRepository


class AuditLogRepository(BaseRepository[AuditLog]):
    """
    Repository responsible for audit log operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        super().__init__(db)

    def _get_model(self) -> type[AuditLog]:
        return AuditLog

    # ---------------------------------------------------------
    # Create / Update
    # ---------------------------------------------------------

    async def create(
        self,
        audit_log: AuditLog,
    ) -> AuditLog:

        self.db.add(audit_log)

        await self.db.flush()

        return audit_log

    async def save(
        self,
        audit_log: AuditLog,
    ) -> AuditLog:

        await self.db.flush()

        return audit_log

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(
        self,
        audit_log_id: UUID,
    ) -> Optional[AuditLog]:

        stmt = (
            select(AuditLog)
            .where(AuditLog.id == audit_log_id)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_public_id(
        self,
        public_id: str,
    ) -> Optional[AuditLog]:

        stmt = (
            select(AuditLog)
            .where(AuditLog.public_id == public_id)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_recent(
        self,
        limit: int = 100,
    ) -> list[AuditLog]:

        stmt = (
            select(AuditLog)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def get_customer_logs(
        self,
        customer_id: UUID,
        limit: int = 100,
    ) -> list[AuditLog]:

        stmt = (
            select(AuditLog)
            .where(AuditLog.customer_id == customer_id)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
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

    # ---------------------------------------------------------
    # Filtering
    # ---------------------------------------------------------

    async def filter_logs(
        self,
        action: Optional[str] = None,
        entity_type: Optional[str] = None,
        customer_id: Optional[UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[AuditLog], int]:

        stmt = select(AuditLog)

        if action:
            stmt = stmt.where(
                AuditLog.action == action
            )

        if entity_type:
            stmt = stmt.where(
                AuditLog.entity_type == entity_type
            )

        if customer_id:
            stmt = stmt.where(
                AuditLog.customer_id == customer_id
            )

        if start_date:
            stmt = stmt.where(
                AuditLog.created_at >= start_date
            )

        if end_date:
            stmt = stmt.where(
                AuditLog.created_at <= end_date
            )

        count_stmt = (
            select(func.count())
            .select_from(stmt.subquery())
        )

        total = await self.db.scalar(
            count_stmt
        ) or 0

        stmt = (
            stmt.order_by(
                AuditLog.created_at.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return (
            list(result.scalars().all()),
            total,
        )