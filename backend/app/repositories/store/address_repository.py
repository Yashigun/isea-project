from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store.address import Address
from app.repositories.base import BaseRepository


class AddressRepository(BaseRepository[Address]):
    """
    Repository responsible for customer address database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[Address]:
        return Address

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(self, address_id: UUID) -> Address | None:
        stmt = select(Address).where(Address.id == address_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, public_id: str) -> Address | None:
        stmt = select(Address).where(Address.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_customer_addresses(self, customer_id: UUID) -> list[Address]:
        stmt = (
            select(Address)
            .where(Address.customer_id == customer_id)
            .order_by(Address.is_default.desc(), Address.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_default_address(self, customer_id: UUID) -> Address | None:
        stmt = (
            select(Address)
            .where(Address.customer_id == customer_id)
            .where(Address.is_default.is_(True))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def count_customer_addresses(self, customer_id: UUID) -> int:
        stmt = select(func.count(Address.id)).where(Address.customer_id == customer_id)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def exists(self, customer_id: UUID, address_id: UUID) -> bool:
        stmt = (
            select(Address.id)
            .where(Address.customer_id == customer_id)
            .where(Address.id == address_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None