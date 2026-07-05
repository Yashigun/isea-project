from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.store.phone_number import PhoneNumber
from app.repositories.base import BaseRepository
from app.models.store.product import Product

class PhoneRepository(BaseRepository[PhoneNumber]):
    """
    Repository responsible for customer phone number database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[PhoneNumber]:
        return PhoneNumber

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(self, phone_id: UUID) -> PhoneNumber | None:
        stmt = select(PhoneNumber).where(PhoneNumber.id == phone_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, public_id: str) -> PhoneNumber | None:
        stmt = select(PhoneNumber).where(PhoneNumber.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_customer_phone_numbers(self, customer_id: UUID) -> list[PhoneNumber]:
        stmt = (
            select(PhoneNumber)
            .where(PhoneNumber.customer_id == customer_id)
            .order_by(PhoneNumber.is_default.desc(), PhoneNumber.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_default_phone(self, customer_id: UUID) -> PhoneNumber | None:
        stmt = (
            select(PhoneNumber)
            .where(PhoneNumber.customer_id == customer_id)
            .where(PhoneNumber.is_default.is_(True))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def count_customer_phone_numbers(self, customer_id: UUID) -> int:
        stmt = select(func.count(PhoneNumber.id)).where(PhoneNumber.customer_id == customer_id)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def belongs_to_customer(self, customer_id: UUID, phone_id: UUID) -> bool:
        stmt = (
            select(PhoneNumber.id)
            .where(PhoneNumber.customer_id == customer_id)
            .where(PhoneNumber.id == phone_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def get_by_phone_number(self, phone_number: str) -> PhoneNumber | None:
        stmt = select(PhoneNumber).where(PhoneNumber.phone_number == phone_number)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_phone_number(self, phone_number: str) -> bool:
        stmt = select(PhoneNumber.id).where(PhoneNumber.phone_number == phone_number)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    async def list_active(self) -> list[Product]:
        stmt = (
            select(Product)
            .where(Product.is_active.is_(True))
            .options(
                selectinload(Product.category),
                selectinload(Product.images),
            )
            .order_by(Product.name.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())