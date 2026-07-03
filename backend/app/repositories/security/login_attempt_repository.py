from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.security.login_attempt import LoginAttempt
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

    async def create(self, attempt: LoginAttempt) -> LoginAttempt:
        self.db.add(attempt)
        await self.db.flush()
        return attempt

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(self, attempt_id: UUID) -> LoginAttempt | None:
        stmt = select(LoginAttempt).where(LoginAttempt.id == attempt_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, public_id: str) -> LoginAttempt | None:
        stmt = select(LoginAttempt).where(LoginAttempt.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_customer_attempts(self, customer_id: UUID, limit: int = 20) -> list[LoginAttempt]:
        stmt = (
            select(LoginAttempt)
            .where(LoginAttempt.customer_id == customer_id)
            .order_by(LoginAttempt.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_ip_attempts(self, ip_address: str, limit: int = 100) -> list[LoginAttempt]:
        stmt = (
            select(LoginAttempt)
            .where(LoginAttempt.ip_address == ip_address)
            .order_by(LoginAttempt.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_recent_failures(self, since: datetime) -> list[LoginAttempt]:
        stmt = (
            select(LoginAttempt)
            .where(LoginAttempt.success.is_(False))
            .where(LoginAttempt.created_at >= since)
            .order_by(LoginAttempt.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    async def count_recent_failures(self, ip_address: str, since: datetime) -> int:
        stmt = (
            select(func.count(LoginAttempt.id))
            .where(LoginAttempt.ip_address == ip_address)
            .where(LoginAttempt.success.is_(False))
            .where(LoginAttempt.created_at >= since)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_customer_failures(self, customer_id: UUID, since: datetime) -> int:
        stmt = (
            select(func.count(LoginAttempt.id))
            .where(LoginAttempt.customer_id == customer_id)
            .where(LoginAttempt.success.is_(False))
            .where(LoginAttempt.created_at >= since)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_ip_attempts(self, ip_address: str, since: datetime) -> int:
        stmt = (
            select(func.count(LoginAttempt.id))
            .where(LoginAttempt.ip_address == ip_address)
            .where(LoginAttempt.created_at >= since)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0