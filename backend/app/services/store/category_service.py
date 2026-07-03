from __future__ import annotations

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.store.category_repository import CategoryRepository
from app.models.store.category import Category
from app.schemas.category import CategoryCreateSchema, CategoryUpdateSchema


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = CategoryRepository(db)

    async def list_active(self) -> List[Category]:
        return await self.repo.get_active_categories()

    async def list_all(self) -> List[Category]:
        return await self.repo.get_all()

    async def get_by_public_id(self, public_id: str) -> Optional[Category]:
        return await self.repo.get_active_by_public_id(public_id)

    async def get_by_slug(self, slug: str) -> Optional[Category]:
        return await self.repo.get_active_by_slug(slug)

    async def create(self, data: CategoryCreateSchema) -> Category:
        # Check uniqueness
        if await self.repo.exists_by_slug(data.slug):
            raise ValueError("Slug already exists")
        if await self.repo.exists_by_name(data.name):
            raise ValueError("Name already exists")
        category = Category(
            name=data.name,
            slug=data.slug,
            description=data.description,
            is_active=data.is_active,
        )
        await self.repo.create(category)
        await self.db.commit()
        return category

    async def update(self, public_id: str, data: CategoryUpdateSchema) -> Category:
        category = await self.repo.get_by_public_id(public_id)
        if not category:
            raise ValueError("Category not found")
        if data.name is not None:
            if data.name != category.name and await self.repo.exists_by_name(data.name):
                raise ValueError("Name already exists")
            category.name = data.name
        if data.slug is not None:
            if data.slug != category.slug and await self.repo.exists_by_slug(data.slug):
                raise ValueError("Slug already exists")
            category.slug = data.slug
        if data.description is not None:
            category.description = data.description
        if data.is_active is not None:
            category.is_active = data.is_active
        await self.repo.save(category)
        await self.db.commit()
        return category

    async def delete(self, public_id: str) -> None:
        category = await self.repo.get_by_public_id(public_id)
        if not category:
            raise ValueError("Category not found")
        # Optionally check if any products are linked to this category
        # If you want to prevent deletion when products exist, add that logic.
        await self.repo.remove(category)
        await self.db.commit()