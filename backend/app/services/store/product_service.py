from __future__ import annotations

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.store.product_repository import ProductRepository
from app.repositories.store.category_repository import CategoryRepository
from app.repositories.store.product_image_repository import ProductImageRepository
from app.models.store.product import Product
from app.models.store.product_image import ProductImage
from app.schemas.product import ProductCreateSchema, ProductUpdateSchema


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.product_repo = ProductRepository(db)
        self.category_repo = CategoryRepository(db)
        self.image_repo = ProductImageRepository(db)

    # ----- Public Methods -----

    async def get_by_public_id(self, public_id: str) -> Optional[Product]:
        return await self.product_repo.get_active_by_public_id(public_id)

    async def get_by_slug(self, slug: str) -> Optional[Product]:
        return await self.product_repo.get_active_by_slug(slug)

    async def list_active(self) -> List[Product]:
        return await self.product_repo.list_active()

    async def list_by_category(self, category_public_id: str) -> List[Product]:
        category = await self.category_repo.get_active_by_public_id(category_public_id)
        if not category:
            return []
        return await self.product_repo.list_by_category(category.id)

    async def search(self, query: str) -> List[Product]:
        return await self.product_repo.search(query)

    async def get_related(self, product_id: UUID, limit: int = 4) -> List[Product]:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            return []
        return await self.product_repo.get_related_products(product.category_id, product_id, limit)

    # ----- Admin Methods -----

    async def create(self, data: ProductCreateSchema) -> Product:
        category = await self.category_repo.get_active_by_public_id(data.category_public_id)
        if not category:
            raise ValueError("Category not found")

        if await self.product_repo.exists_by_slug(data.slug):
            raise ValueError("Slug already exists")

        product = Product(
            category_id=category.id,
            name=data.name,
            slug=data.slug,
            short_description=data.short_description,
            description=data.description,
            price=data.price,
            discount_price=data.discount_price,
            is_active=data.is_active,
        )
        await self.product_repo.create(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def update(self, public_id: str, data: ProductUpdateSchema) -> Product:
        product = await self.product_repo.get_by_public_id(public_id)
        if not product:
            raise ValueError("Product not found")

        if data.category_public_id:
            category = await self.category_repo.get_active_by_public_id(data.category_public_id)
            if not category:
                raise ValueError("Category not found")
            product.category_id = category.id

        if data.name is not None:
            product.name = data.name
        if data.slug is not None:
            if await self.product_repo.exists_by_slug(data.slug):
                raise ValueError("Slug already exists")
            product.slug = data.slug
        if data.short_description is not None:
            product.short_description = data.short_description
        if data.description is not None:
            product.description = data.description
        if data.price is not None:
            product.price = data.price
        if data.discount_price is not None:
            product.discount_price = data.discount_price
        if data.is_active is not None:
            product.is_active = data.is_active

        await self.product_repo.save(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete(self, public_id: str) -> None:
        product = await self.product_repo.get_by_public_id(public_id)
        if not product:
            raise ValueError("Product not found")
        await self.product_repo.remove(product)
        await self.db.commit()

    # ----- Image Handling -----

    async def add_image(self, product_public_id: str, image_data: dict) -> ProductImage:
        product = await self.product_repo.get_by_public_id(product_public_id)
        if not product:
            raise ValueError("Product not found")

        url = image_data.get("url")
        if not url:
            raise ValueError("Image URL is required")

        # Check if this should be primary (first image)
        existing_images = await self.image_repo.get_product_images(product.id)
        is_primary = image_data.get("is_primary", False)
        if not existing_images:
            is_primary = True

        display_order = image_data.get("display_order", len(existing_images) + 1)

        image = ProductImage(
            product_id=product.id,
            url=url,
            stored_filename=image_data.get("stored_filename", ""),
            original_filename=image_data.get("original_filename", ""),
            mime_type=image_data.get("mime_type", ""),
            file_size=image_data.get("file_size", 0),
            sha256_hash=image_data.get("sha256_hash", ""),
            alt_text=image_data.get("alt_text"),
            display_order=display_order,
            is_primary=is_primary,
        )
        await self.image_repo.create(image)
        await self.db.commit()
        await self.db.refresh(image)
        return image