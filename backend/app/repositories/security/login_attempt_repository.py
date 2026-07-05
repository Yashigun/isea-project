from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.security.login_attempt import (
    LoginAttempt,
    AttemptType,
)
from app.repositories.base import BaseRepository


class LoginAttemptRepository(BaseRepository[LoginAttempt]):
    """
    Repository responsible for login attempt database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[LoginAttempt]:
        return LoginAttempt

    # ---------------------------------------------------------
    # Create
    # ---------------------------------------------------------

    async def create(
        self,
        attempt: LoginAttempt,
    ) -> LoginAttempt:
        self.db.add(attempt)
        await self.db.flush()
        return attempt

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(
        self,
        attempt_id: UUID,
    ) -> Optional[LoginAttempt]:

        stmt = (
            select(LoginAttempt)
            .where(LoginAttempt.id == attempt_id)
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(
        self,
        public_id: str,
    ) -> Optional[LoginAttempt]:

        stmt = (
            select(LoginAttempt)
            .where(LoginAttempt.public_id == public_id)
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_customer_attempts(
        self,
        customer_id: UUID,
        limit: int = 20,
    ) -> list[LoginAttempt]:

        stmt = (
            select(LoginAttempt)
            .where(LoginAttempt.customer_id == customer_id)
            .order_by(LoginAttempt.created_at.desc())
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_ip_attempts(
        self,
        ip_address: str,
        limit: int = 100,
    ) -> list[LoginAttempt]:

        stmt = (
            select(LoginAttempt)
            .where(LoginAttempt.ip_address == ip_address)
            .order_by(LoginAttempt.created_at.desc())
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_recent_failures(
        self,
        since: datetime,
        limit: int = 100,
    ) -> list[LoginAttempt]:

        stmt = (
            select(LoginAttempt)
            .where(LoginAttempt.successful.is_(False))
            .where(LoginAttempt.created_at >= since)
            .order_by(LoginAttempt.created_at.desc())
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    async def count_recent_failures(
        self,
        since: datetime,
    ) -> int:

        stmt = (
            select(func.count(LoginAttempt.id))
            .where(LoginAttempt.successful.is_(False))
            .where(LoginAttempt.created_at >= since)
        )

        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_customer_failures(
        self,
        customer_id: UUID,
        since: datetime,
    ) -> int:

        stmt = (
            select(func.count(LoginAttempt.id))
            .where(LoginAttempt.customer_id == customer_id)
            .where(LoginAttempt.successful.is_(False))
            .where(LoginAttempt.created_at >= since)
        )

        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_ip_attempts(
        self,
        ip_address: str,
        since: datetime,
    ) -> int:

        stmt = (
            select(func.count(LoginAttempt.id))
            .where(LoginAttempt.ip_address == ip_address)
            .where(LoginAttempt.created_at >= since)
        )

        result = await self.db.execute(stmt)
        return result.scalar() or 0

    # ---------------------------------------------------------
    # Filtering
    # ---------------------------------------------------------

    async def filter_attempts(
        self,
        email: Optional[str] = None,
        ip: Optional[str] = None,
        successful: Optional[bool] = None,
        attempt_type: Optional[AttemptType | str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[LoginAttempt], int]:

        stmt = select(LoginAttempt)

        if email:
            stmt = stmt.where(LoginAttempt.email == email)

        if ip:
            stmt = stmt.where(LoginAttempt.ip_address == ip)

        if successful is not None:
            stmt = stmt.where(
                LoginAttempt.successful == successful
            )

        if attempt_type:
            stmt = stmt.where(
                LoginAttempt.attempt_type == attempt_type
            )

        if start_date:
            stmt = stmt.where(
                LoginAttempt.created_at >= start_date
            )

        if end_date:
            stmt = stmt.where(
                LoginAttempt.created_at <= end_date
            )

        count_stmt = (
            select(func.count())
            .select_from(stmt.subquery())
        )

        total = await self.db.scalar(count_stmt) or 0

        stmt = (
            stmt.order_by(LoginAttempt.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return (
            list(result.scalars().all()),
            total,
        )
        
    async def count_recent_failures_all(self, since: datetime) -> int:
        """
        Count all failed login attempts since the given time, regardless of IP.
        """
        stmt = (
            select(func.count(LoginAttempt.id))
            .where(LoginAttempt.successful.is_(False))
            .where(LoginAttempt.created_at >= since)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0