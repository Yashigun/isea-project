from __future__ import annotations

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.store.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """
    Repository responsible for product database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[Product]:
        return Product

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(self, product_id) -> Product | None:
        stmt = select(Product).where(Product.id == product_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, public_id: str) -> Product | None:
        stmt = select(Product).where(Product.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Product | None:
        stmt = select(Product).where(Product.slug == slug)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_slug(self, slug: str) -> bool:
        stmt = select(Product.id).where(Product.slug == slug)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def list_active(self) -> list[Product]:
        stmt = (
            select(Product)
            .where(Product.is_active.is_(True))
            .order_by(Product.name.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_by_category(self, category_id) -> list[Product]:
        stmt = (
            select(Product)
            .where(Product.category_id == category_id)
            .where(Product.is_active.is_(True))
            .order_by(Product.name.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def search(self, query: str) -> list[Product]:
        pattern = f"%{query}%"
        stmt = (
            select(Product)
            .where(Product.is_active.is_(True))
            .where(
                or_(
                    Product.name.ilike(pattern),
                    Product.short_description.ilike(pattern),
                    Product.description.ilike(pattern),
                )
            )
            .order_by(Product.name.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_details_by_public_id(self, public_id: str) -> Product | None:
        stmt = (
            select(Product)
            .options(
                selectinload(Product.category),
                selectinload(Product.images),
                selectinload(Product.reviews),
            )
            .where(Product.public_id == public_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_related_products(self, category_id, exclude_product_id, limit: int = 4) -> list[Product]:
        stmt = (
            select(Product)
            .where(Product.category_id == category_id)
            .where(Product.id != exclude_product_id)
            .where(Product.is_active.is_(True))
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_active_by_slug(self, slug: str) -> Product | None:
        stmt = (
            select(Product)
            .options(
                selectinload(Product.category),
                selectinload(Product.images),
                selectinload(Product.reviews),
            )
            .where(Product.slug == slug)
            .where(Product.is_active.is_(True))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_by_public_id(self, public_id: str) -> Product | None:
        stmt = (
            select(Product)
            .options(
                selectinload(Product.category),
                selectinload(Product.images),
                selectinload(Product.reviews),
            )
            .where(Product.public_id == public_id)
            .where(Product.is_active.is_(True))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()