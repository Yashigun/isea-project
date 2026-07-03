from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.security.request_log import RequestLog
from app.repositories.base import BaseRepository


class RequestLogRepository(BaseRepository[RequestLog]):
    """
    Repository responsible for HTTP request logging and forensic queries.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[RequestLog]:
        return RequestLog

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(self, request_log_id: UUID) -> RequestLog | None:
        stmt = select(RequestLog).where(RequestLog.id == request_log_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, public_id: str) -> RequestLog | None:
        stmt = select(RequestLog).where(RequestLog.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_recent(self, limit: int = 100) -> list[RequestLog]:
        stmt = select(RequestLog).order_by(RequestLog.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_customer_requests(self, customer_id: UUID, limit: int = 100) -> list[RequestLog]:
        stmt = (
            select(RequestLog)
            .where(RequestLog.customer_id == customer_id)
            .order_by(RequestLog.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_ip_requests(self, ip_address: str, limit: int = 100) -> list[RequestLog]:
        stmt = (
            select(RequestLog)
            .where(RequestLog.ip_address == ip_address)
            .order_by(RequestLog.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_between(self, start_time: datetime, end_time: datetime) -> list[RequestLog]:
        stmt = (
            select(RequestLog)
            .where(RequestLog.created_at >= start_time)
            .where(RequestLog.created_at <= end_time)
            .order_by(RequestLog.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_method(self, method: str, limit: int = 100) -> list[RequestLog]:
        # Note: method is stored as enum, but we can compare with string
        stmt = (
            select(RequestLog)
            .where(RequestLog.method == method)   # enum comparison works with string value
            .order_by(RequestLog.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_status_code(self, status_code: int, limit: int = 100) -> list[RequestLog]:
        stmt = (
            select(RequestLog)
            .where(RequestLog.status_code == status_code)
            .order_by(RequestLog.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    async def count_requests(self) -> int:
        stmt = select(func.count(RequestLog.id))
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_ip_requests(self, ip_address: str, since: datetime) -> int:
        stmt = (
            select(func.count(RequestLog.id))
            .where(RequestLog.ip_address == ip_address)
            .where(RequestLog.created_at >= since)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_customer_requests(self, customer_id: UUID, since: datetime) -> int:
        stmt = (
            select(func.count(RequestLog.id))
            .where(RequestLog.customer_id == customer_id)
            .where(RequestLog.created_at >= since)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_status_code(self, status_code: int, since: datetime) -> int:
        stmt = (
            select(func.count(RequestLog.id))
            .where(RequestLog.status_code == status_code)
            .where(RequestLog.created_at >= since)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0
    
    async def count_requests_since(self, since: datetime) -> int:
        stmt = select(func.count(RequestLog.id)).where(RequestLog.created_at >= since)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_top_ips(self, limit: int = 10) -> list[tuple[str, int]]:
        stmt = (
            select(RequestLog.ip_address, func.count(RequestLog.id))
            .group_by(RequestLog.ip_address)
            .order_by(func.count(RequestLog.id).desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.all()