from __future__ import annotations

from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.store.wishlist_repository import WishlistRepository
from app.repositories.store.product_repository import ProductRepository
from app.models.store.wishlist_item import WishlistItem
from app.models.store.product import Product


class WishlistService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = WishlistRepository(db)
        self.product_repo = ProductRepository(db)

    async def get_customer_wishlist(self, customer_id: UUID) -> List[WishlistItem]:
        return await self.repo.get_customer_wishlist(customer_id)

    async def add_item(self, customer_id: UUID, product_public_id: str) -> WishlistItem:
        product = await self.product_repo.get_active_by_public_id(product_public_id)
        if not product:
            raise ValueError("Product not found")
        # Check if already in wishlist
        existing = await self.repo.get_item(customer_id, product.id)
        if existing:
            raise ValueError("Product already in wishlist")
        item = WishlistItem(
            customer_id=customer_id,
            product_id=product.id,
        )
        await self.repo.create(item)
        await self.db.commit()
        return item

    async def remove_item(self, customer_id: UUID, product_public_id: str) -> None:
        product = await self.product_repo.get_active_by_public_id(product_public_id)
        if not product:
            raise ValueError("Product not found")
        item = await self.repo.get_item(customer_id, product.id)
        if not item:
            raise ValueError("Item not in wishlist")
        await self.repo.remove(item)
        await self.db.commit()