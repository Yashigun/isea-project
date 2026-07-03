from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.store.wishlist_item import WishlistItem
from app.repositories.base import BaseRepository


class WishlistRepository(BaseRepository[WishlistItem]):
    """
    Repository responsible for customer wishlist database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[WishlistItem]:
        return WishlistItem

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(self, wishlist_item_id: UUID) -> WishlistItem | None:
        stmt = select(WishlistItem).where(WishlistItem.id == wishlist_item_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_customer_wishlist(self, customer_id: UUID) -> list[WishlistItem]:
        stmt = (
            select(WishlistItem)
            .options(selectinload(WishlistItem.product))
            .where(WishlistItem.customer_id == customer_id)
            .order_by(WishlistItem.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_item(self, customer_id: UUID, product_id: UUID) -> WishlistItem | None:
        stmt = (
            select(WishlistItem)
            .where(WishlistItem.customer_id == customer_id)
            .where(WishlistItem.product_id == product_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def exists(self, customer_id: UUID, product_id: UUID) -> bool:
        stmt = (
            select(WishlistItem.id)
            .where(WishlistItem.customer_id == customer_id)
            .where(WishlistItem.product_id == product_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def count_customer_items(self, customer_id: UUID) -> int:
        stmt = select(WishlistItem.id).where(WishlistItem.customer_id == customer_id)
        result = await self.db.execute(stmt)
        return len(result.scalars().all())