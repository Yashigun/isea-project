from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.security.blocked_ip import BlockedIP
from app.repositories.base import BaseRepository


class BlockedIPRepository(BaseRepository[BlockedIP]):
    """
    Repository responsible for blocked IP database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        super().__init__(db)

    def _get_model(self) -> type[BlockedIP]:
        return BlockedIP

    # ---------------------------------------------------------
    # Create / Update
    # ---------------------------------------------------------

    async def create(
        self,
        blocked_ip: BlockedIP,
    ) -> BlockedIP:

        self.db.add(blocked_ip)

        await self.db.flush()

        return blocked_ip

    async def save(
        self,
        blocked_ip: BlockedIP,
    ) -> BlockedIP:

        await self.db.flush()

        return blocked_ip

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(
        self,
        blocked_ip_id: UUID,
    ) -> Optional[BlockedIP]:

        stmt = (
            select(BlockedIP)
            .where(BlockedIP.id == blocked_ip_id)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_public_id(
        self,
        public_id: str,
    ) -> Optional[BlockedIP]:

        stmt = (
            select(BlockedIP)
            .where(BlockedIP.public_id == public_id)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_ip_address(
        self,
        ip_address: str,
    ) -> Optional[BlockedIP]:

        stmt = (
            select(BlockedIP)
            .where(BlockedIP.ip_address == ip_address)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def list_active_blocks(
        self,
        now: datetime,
    ) -> list[BlockedIP]:

        stmt = (
            select(BlockedIP)
            .where(BlockedIP.is_active.is_(True))
            .where(
                or_(
                    BlockedIP.permanently_blocked.is_(True),
                    BlockedIP.blocked_until > now,
                )
            )
            .order_by(BlockedIP.created_at.desc())
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    async def count_active_blocks(
        self,
        now: datetime,
    ) -> int:

        stmt = (
            select(func.count(BlockedIP.id))
            .where(BlockedIP.is_active.is_(True))
            .where(
                or_(
                    BlockedIP.permanently_blocked.is_(True),
                    BlockedIP.blocked_until > now,
                )
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar() or 0