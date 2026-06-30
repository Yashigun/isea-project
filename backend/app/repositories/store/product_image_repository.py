from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.store.product_image import ProductImage
from app.repositories.base import BaseRepository


class ProductImageRepository(
    BaseRepository[ProductImage],
):
    """
    Repository responsible for product image
    database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    def get_by_id(
        self,
        image_id: UUID,
    ) -> ProductImage | None:

        statement = (
            select(ProductImage)
            .where(
                ProductImage.id == image_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_public_id(
        self,
        public_id: str,
    ) -> ProductImage | None:

        statement = (
            select(ProductImage)
            .where(
                ProductImage.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_stored_filename(
        self,
        stored_filename: str,
    ) -> ProductImage | None:

        statement = (
            select(ProductImage)
            .where(
                ProductImage.stored_filename == stored_filename,
            )
        )

        return self.db.scalar(statement)

    def get_by_sha256_hash(
        self,
        sha256_hash: str,
    ) -> ProductImage | None:

        statement = (
            select(ProductImage)
            .where(
                ProductImage.sha256_hash == sha256_hash,
            )
        )

        return self.db.scalar(statement)

    def get_primary_image(
        self,
        product_id: UUID,
    ) -> ProductImage | None:

        statement = (
            select(ProductImage)
            .where(
                ProductImage.product_id == product_id,
            )
            .where(
                ProductImage.is_primary.is_(True),
            )
        )

        return self.db.scalar(statement)

    def get_product_images(
        self,
        product_id: UUID,
    ) -> list[ProductImage]:

        statement = (
            select(ProductImage)
            .where(
                ProductImage.product_id == product_id,
            )
            .order_by(
                ProductImage.display_order.asc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def exists_by_sha256_hash(
        self,
        sha256_hash: str,
    ) -> bool:

        statement = (
            select(ProductImage.id)
            .where(
                ProductImage.sha256_hash == sha256_hash,
            )
        )

        return self.db.scalar(statement) is not None

    def exists_by_stored_filename(
        self,
        stored_filename: str,
    ) -> bool:

        statement = (
            select(ProductImage.id)
            .where(
                ProductImage.stored_filename == stored_filename,
            )
        )

        return self.db.scalar(statement) is not None