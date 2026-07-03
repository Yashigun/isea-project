from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store.category import Category
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """
    Repository responsible for category database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[Category]:
        return Category

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(self, category_id) -> Category | None:
        stmt = select(Category).where(Category.id == category_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, public_id: str) -> Category | None:
        stmt = select(Category).where(Category.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Category | None:
        stmt = select(Category).where(Category.slug == slug)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Category | None:
        stmt = select(Category).where(Category.name == name)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_slug(self, slug: str) -> bool:
        stmt = select(Category.id).where(Category.slug == slug)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def exists_by_name(self, name: str) -> bool:
        stmt = select(Category.id).where(Category.name == name)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def get_active_categories(self) -> list[Category]:
        stmt = (
            select(Category)
            .where(Category.is_active.is_(True))
            .order_by(Category.name.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_all(self) -> list[Category]:
        stmt = select(Category).order_by(Category.name.asc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_active_by_slug(self, slug: str) -> Category | None:
        stmt = (
            select(Category)
            .where(Category.slug == slug)
            .where(Category.is_active.is_(True))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_by_public_id(self, public_id: str) -> Category | None:
        stmt = (
            select(Category)
            .where(Category.public_id == public_id)
            .where(Category.is_active.is_(True))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_public_id(self, public_id: str) -> bool:
        stmt = select(Category.id).where(Category.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None