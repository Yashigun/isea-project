from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.store.cart import Cart
from app.models.store.cart_item import CartItem
from app.models.store.product import Product
from app.repositories.base import BaseRepository


class CartRepository(BaseRepository[Cart]):
    """
    Repository responsible for shopping cart database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[Cart]:
        return Cart

    # ---------------------------------------------------------
    # Cart
    # ---------------------------------------------------------

    async def get_by_id(self, cart_id: UUID) -> Cart | None:
        stmt = select(Cart).where(Cart.id == cart_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, public_id: str) -> Cart | None:
        stmt = select(Cart).where(Cart.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_customer_cart(self, customer_id: UUID) -> Cart | None:
        stmt = (
            select(Cart)
            .options(
                selectinload(Cart.items).selectinload(CartItem.product).selectinload(Product.category),
                selectinload(Cart.items).selectinload(CartItem.product).selectinload(Product.images),
            )
            .where(Cart.customer_id == customer_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # ---------------------------------------------------------
    # Cart Items
    # ---------------------------------------------------------

    async def get_cart_item(self, cart_id: UUID, product_id: UUID) -> CartItem | None:
        stmt = (
            select(CartItem)
            .where(CartItem.cart_id == cart_id)
            .where(CartItem.product_id == product_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_cart_items(self, cart_id: UUID) -> list[CartItem]:
        stmt = (
            select(CartItem)
            .options(
                selectinload(CartItem.product).selectinload(Product.category),
                selectinload(CartItem.product).selectinload(Product.images),
            )
            .where(CartItem.cart_id == cart_id)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_cart_items(self, cart_id: UUID) -> int:
        stmt = select(func.count(CartItem.id)).where(CartItem.cart_id == cart_id)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_total_quantity(self, cart_id: UUID) -> int:
        stmt = (
            select(func.coalesce(func.sum(CartItem.quantity), 0))
            .where(CartItem.cart_id == cart_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def item_exists(self, cart_id: UUID, product_id: UUID) -> bool:
        stmt = (
            select(CartItem.id)
            .where(CartItem.cart_id == cart_id)
            .where(CartItem.product_id == product_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None
