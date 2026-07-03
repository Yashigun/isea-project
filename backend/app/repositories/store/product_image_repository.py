from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store.product_image import ProductImage
from app.repositories.base import BaseRepository


class ProductImageRepository(BaseRepository[ProductImage]):
    """
    Repository responsible for product image database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[ProductImage]:
        return ProductImage

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(self, image_id: UUID) -> ProductImage | None:
        stmt = select(ProductImage).where(ProductImage.id == image_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, public_id: str) -> ProductImage | None:
        stmt = select(ProductImage).where(ProductImage.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_stored_filename(self, stored_filename: str) -> ProductImage | None:
        stmt = select(ProductImage).where(ProductImage.stored_filename == stored_filename)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_sha256_hash(self, sha256_hash: str) -> ProductImage | None:
        stmt = select(ProductImage).where(ProductImage.sha256_hash == sha256_hash)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_primary_image(self, product_id: UUID) -> ProductImage | None:
        stmt = (
            select(ProductImage)
            .where(ProductImage.product_id == product_id)
            .where(ProductImage.is_primary.is_(True))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_product_images(self, product_id: UUID) -> list[ProductImage]:
        stmt = (
            select(ProductImage)
            .where(ProductImage.product_id == product_id)
            .order_by(ProductImage.display_order.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def exists_by_sha256_hash(self, sha256_hash: str) -> bool:
        stmt = select(ProductImage.id).where(ProductImage.sha256_hash == sha256_hash)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def exists_by_stored_filename(self, stored_filename: str) -> bool:
        stmt = select(ProductImage.id).where(ProductImage.stored_filename == stored_filename)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None