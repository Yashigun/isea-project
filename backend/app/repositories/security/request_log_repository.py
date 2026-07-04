from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.security.request_log import (
    RequestLog,
    HttpMethod,
)
from app.repositories.base import BaseRepository


class RequestLogRepository(BaseRepository[RequestLog]):
    """
    Repository responsible for HTTP request log operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        super().__init__(db)

    def _get_model(self) -> type[RequestLog]:
        return RequestLog

    # ---------------------------------------------------------
    # Create / Update
    # ---------------------------------------------------------

    async def create(
        self,
        request_log: RequestLog,
    ) -> RequestLog:

        self.db.add(request_log)

        await self.db.flush()

        return request_log

    async def save(
        self,
        request_log: RequestLog,
    ) -> RequestLog:

        await self.db.flush()

        return request_log

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(
        self,
        request_log_id: UUID,
    ) -> Optional[RequestLog]:

        stmt = (
            select(RequestLog)
            .where(RequestLog.id == request_log_id)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_public_id(
        self,
        public_id: str,
    ) -> Optional[RequestLog]:

        stmt = (
            select(RequestLog)
            .where(RequestLog.public_id == public_id)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_recent(
        self,
        limit: int = 100,
    ) -> list[RequestLog]:

        stmt = (
            select(RequestLog)
            .order_by(RequestLog.created_at.desc())
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def get_customer_requests(
        self,
        customer_id: UUID,
        limit: int = 100,
    ) -> list[RequestLog]:

        stmt = (
            select(RequestLog)
            .where(RequestLog.customer_id == customer_id)
            .order_by(RequestLog.created_at.desc())
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def get_ip_requests(
        self,
        ip_address: str,
        limit: int = 100,
    ) -> list[RequestLog]:

        stmt = (
            select(RequestLog)
            .where(RequestLog.ip_address == ip_address)
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

    async def count_requests_since(
        self,
        since: datetime,
    ) -> int:

        stmt = (
            select(func.count(RequestLog.id))
            .where(RequestLog.created_at >= since)
        )

        result = await self.db.execute(stmt)

        return result.scalar() or 0

    async def count_ip_requests(
        self,
        ip_address: str,
        since: datetime,
    ) -> int:

        stmt = (
            select(func.count(RequestLog.id))
            .where(RequestLog.ip_address == ip_address)
            .where(RequestLog.created_at >= since)
        )

        result = await self.db.execute(stmt)

        return result.scalar() or 0

    async def get_top_ips(
        self,
        limit: int = 10,
    ) -> list[tuple[str, int]]:

        stmt = (
            select(
                RequestLog.ip_address,
                func.count(RequestLog.id),
            )
            .group_by(RequestLog.ip_address)
            .order_by(
                func.count(RequestLog.id).desc()
            )
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return result.all()

    # ---------------------------------------------------------
    # Filtering
    # ---------------------------------------------------------

    async def filter_logs(
        self,
        method: Optional[HttpMethod | str] = None,
        status_code: Optional[int] = None,
        ip: Optional[str] = None,
        customer_id: Optional[UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[RequestLog], int]:

        stmt = select(RequestLog)

        if method:
            stmt = stmt.where(
                RequestLog.method == method
            )

        if status_code is not None:
            stmt = stmt.where(
                RequestLog.status_code == status_code
            )

        if ip:
            stmt = stmt.where(
                RequestLog.ip_address == ip
            )

        if customer_id:
            stmt = stmt.where(
                RequestLog.customer_id == customer_id
            )

        if start_date:
            stmt = stmt.where(
                RequestLog.created_at >= start_date
            )

        if end_date:
            stmt = stmt.where(
                RequestLog.created_at <= end_date
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
                RequestLog.created_at.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return (
            list(result.scalars().all()),
            total,
        )