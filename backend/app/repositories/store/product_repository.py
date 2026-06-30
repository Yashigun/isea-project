from __future__ import annotations

from sqlalchemy import (
    or_,
    select,
)

from sqlalchemy.orm import (
    Session,
    selectinload,
)

from app.models.store.product import (
    Product,
)

from app.repositories.base import (
    BaseRepository,
)


class ProductRepository(
    BaseRepository[Product],
):
    """
    Repository responsible for product
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
        product_id,
    ) -> Product | None:

        statement = (
            select(Product)
            .where(
                Product.id == product_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_public_id(
        self,
        public_id: str,
    ) -> Product | None:

        statement = (
            select(Product)
            .where(
                Product.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_slug(
        self,
        slug: str,
    ) -> Product | None:

        statement = (
            select(Product)
            .where(
                Product.slug == slug,
            )
        )

        return self.db.scalar(statement)

    def exists_by_slug(
        self,
        slug: str,
    ) -> bool:

        statement = (
            select(Product.id)
            .where(
                Product.slug == slug,
            )
        )

        return self.db.scalar(statement) is not None

    def list_active(
        self,
    ) -> list[Product]:

        statement = (
            select(Product)
            .where(
                Product.is_active.is_(True),
            )
            .order_by(
                Product.name.asc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def list_by_category(
        self,
        category_id,
    ) -> list[Product]:

        statement = (
            select(Product)
            .where(
                Product.category_id == category_id,
            )
            .where(
                Product.is_active.is_(True),
            )
            .order_by(
                Product.name.asc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def search(
        self,
        query: str,
    ) -> list[Product]:

        pattern = f"%{query}%"

        statement = (
            select(Product)
            .where(
                Product.is_active.is_(True),
            )
            .where(
                or_(
                    Product.name.ilike(pattern),
                    Product.short_description.ilike(pattern),
                    Product.description.ilike(pattern),
                )
            )
            .order_by(
                Product.name.asc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def get_product_details(
        self,
        public_id: str,
    ) -> Product | None:

        statement = (
            select(Product)
            .options(
                selectinload(Product.category),
                selectinload(Product.images),
                selectinload(Product.reviews),
            )
            .where(
                Product.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_related_products(
        self,
        category_id,
        exclude_product_id,
        limit: int = 4,
    ) -> list[Product]:

        statement = (
            select(Product)
            .where(
                Product.category_id == category_id,
            )
            .where(
                Product.id != exclude_product_id,
            )
            .where(
                Product.is_active.is_(True),
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(statement)
        )