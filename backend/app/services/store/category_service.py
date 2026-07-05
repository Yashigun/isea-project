from __future__ import annotations

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store.category import Category

from app.repositories.store.category_repository import CategoryRepository
from app.repositories.store.product_repository import ProductRepository

from app.schemas.category import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
)


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

        self.repo = CategoryRepository(db)
        self.product_repo = ProductRepository(db)

    # --------------------------------------------------------
    # Public
    # --------------------------------------------------------

    async def _set_category_image(self, category: Category) -> None:
        products = await self.product_repo.list_by_category(category.id)
        for product in products:
            if product.images:
                setattr(category, "_image", product.images[0].url)
                return
        setattr(category, "_image", "/placeholder.jpg")

    async def list_active(self):
        categories = await self.repo.get_active_categories()
        for category in categories:
            await self._set_category_image(category)
        return categories

    async def list_all(self):
        categories = await self.repo.get_all()
        for category in categories:
            await self._set_category_image(category)
        return categories

    async def get_by_public_id(
        self,
        public_id: str,
    ) -> Optional[Category]:

        category = await self.repo.get_by_public_id(public_id)
        if category is not None:
            await self._set_category_image(category)
        return category

    async def get_by_slug(
        self,
        slug: str,
    ) -> Optional[Category]:

        category = await self.repo.get_by_slug(slug)
        if category is not None:
            await self._set_category_image(category)
        return category

    # --------------------------------------------------------
    # Admin
    # --------------------------------------------------------

    async def create(
        self,
        data: CategoryCreateSchema,
    ) -> Category:

        if await self.repo.exists_by_slug(data.slug):
            raise ValueError("Slug already exists")

        if await self.repo.exists_by_name(data.name):
            raise ValueError("Category name already exists")

        category = Category(
            name=data.name,
            slug=data.slug,
            description=data.description,
            is_active=data.is_active,
        )

        await self.repo.create(category)

        await self.db.commit()

        await self.db.refresh(category)

        return category

    async def update(
        self,
        public_id: str,
        data: CategoryUpdateSchema,
    ) -> Category:

        category = await self.repo.get_by_public_id(public_id)

        if category is None:
            raise ValueError("Category not found")

        if data.name is not None:

            existing = await self.repo.get_by_name(data.name)

            if (
                existing is not None
                and existing.public_id != category.public_id
            ):
                raise ValueError("Category name already exists")

            category.name = data.name

        if data.slug is not None:

            existing = await self.repo.get_by_slug(data.slug)

            if (
                existing is not None
                and existing.public_id != category.public_id
            ):
                raise ValueError("Slug already exists")

            category.slug = data.slug

        if data.description is not None:
            category.description = data.description

        if data.is_active is not None:
            category.is_active = data.is_active

        await self.repo.save(category)

        await self.db.commit()

        await self.db.refresh(category)

        return category

    async def delete(
        self,
        public_id: str,
    ):

        category = await self.repo.get_by_public_id(public_id)

        if category is None:
            raise ValueError("Category not found")

        products = await self.product_repo.list_by_category(category.id)

        if products:
            raise ValueError(
                "Cannot delete category that contains products."
            )

        await self.repo.remove(category)

        await self.db.commit()
