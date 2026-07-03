from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.security.blocked_ip import BlockedIP
from app.repositories.base import BaseRepository


class BlockedIPRepository(BaseRepository[BlockedIP]):
    """
    Repository responsible for blocked IP database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[BlockedIP]:
        return BlockedIP

    # ---------------------------------------------------------
    # Private Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _active_block_condition(current_time: datetime):
        """
        Active blocks include:
        - Permanent blocks (blocked_until IS NULL)
        - Temporary blocks that have not expired.
        """
        return and_(
            BlockedIP.is_active.is_(True),
            or_(
                BlockedIP.blocked_until.is_(None),
                BlockedIP.blocked_until > current_time,
            ),
        )

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(self, blocked_ip_id: UUID) -> BlockedIP | None:
        stmt = select(BlockedIP).where(BlockedIP.id == blocked_ip_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, public_id: str) -> BlockedIP | None:
        stmt = select(BlockedIP).where(BlockedIP.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_ip_address(self, ip_address: str) -> BlockedIP | None:
        stmt = select(BlockedIP).where(BlockedIP.ip_address == ip_address)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_block(self, ip_address: str, current_time: datetime) -> BlockedIP | None:
        stmt = (
            select(BlockedIP)
            .where(BlockedIP.ip_address == ip_address)
            .where(self._active_block_condition(current_time))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_recent_blocks(self, limit: int = 100) -> list[BlockedIP]:
        stmt = select(BlockedIP).order_by(BlockedIP.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_active_blocks(self, current_time: datetime) -> list[BlockedIP]:
        stmt = (
            select(BlockedIP)
            .where(self._active_block_condition(current_time))
            .order_by(BlockedIP.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_expired_blocks(self, current_time: datetime) -> list[BlockedIP]:
        stmt = (
            select(BlockedIP)
            .where(BlockedIP.is_active.is_(True))
            .where(BlockedIP.blocked_until.is_not(None))
            .where(BlockedIP.blocked_until <= current_time)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def exists_by_ip(self, ip_address: str) -> bool:
        stmt = select(BlockedIP.id).where(BlockedIP.ip_address == ip_address)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    async def count_active_blocks(self, current_time: datetime) -> int:
        stmt = select(func.count(BlockedIP.id)).where(self._active_block_condition(current_time))
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_expired_blocks(self, current_time: datetime) -> int:
        stmt = (
            select(func.count(BlockedIP.id))
            .where(BlockedIP.is_active.is_(True))
            .where(BlockedIP.blocked_until.is_not(None))
            .where(BlockedIP.blocked_until <= current_time)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_permanent_blocks(self) -> int:
        stmt = (
            select(func.count(BlockedIP.id))
            .where(BlockedIP.is_active.is_(True))
            .where(BlockedIP.blocked_until.is_(None))
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0