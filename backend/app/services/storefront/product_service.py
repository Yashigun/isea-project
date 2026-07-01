from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.store.category_repository import (
    CategoryRepository,
)

from app.repositories.store.product_repository import (
    ProductRepository,
)

from app.schemas.product import (
    ProductResponseSchema,
)

from app.services.base import BaseService


class ProductService(BaseService):
    """
    Customer-facing product service.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

        self.product_repository = (
            ProductRepository(db)
        )

        self.category_repository = (
            CategoryRepository(db)
        )

    # ---------------------------------------------------------
    # Products
    # ---------------------------------------------------------

    def list_products(
        self,
    ) -> list[ProductResponseSchema]:

        products = (
            self.product_repository.list_active()
        )

        return self.to_schema_list(
            products,
            ProductResponseSchema,
        )

    def get_product_by_slug(
        self,
        slug: str,
    ) -> ProductResponseSchema | None:

        product = (
            self.product_repository.get_active_by_slug(
                slug,
            )
        )

        if product is None:
            return None

        return self.to_schema(
            product,
            ProductResponseSchema,
        )

    def get_product_by_public_id(
        self,
        public_id: str,
    ) -> ProductResponseSchema | None:

        product = (
            self.product_repository.get_active_by_public_id(
                public_id,
            )
        )

        if product is None:
            return None

        return self.to_schema(
            product,
            ProductResponseSchema,
        )

    def search_products(
        self,
        query: str,
    ) -> list[ProductResponseSchema]:

        products = (
            self.product_repository.search(
                query,
            )
        )

        return self.to_schema_list(
            products,
            ProductResponseSchema,
        )

    def get_products_by_category(
        self,
        category_slug: str,
    ) -> list[ProductResponseSchema]:

        category = (
            self.category_repository.get_active_by_slug(
                category_slug,
            )
        )

        if category is None:
            return []

        products = (
            self.product_repository.list_by_category(
                category.id,
            )
        )

        return self.to_schema_list(
            products,
            ProductResponseSchema,
        )

    def get_related_products(
        self,
        slug: str,
        limit: int = 4,
    ) -> list[ProductResponseSchema]:

        product = (
            self.product_repository.get_active_by_slug(
                slug,
            )
        )

        if product is None:
            return []

        related_products = (
            self.product_repository.get_related_products(
                category_id=product.category_id,
                exclude_product_id=product.id,
                limit=limit,
            )
        )

        return self.to_schema_list(
            related_products,
            ProductResponseSchema,
        )

    def product_exists(
        self,
        slug: str,
    ) -> bool:

        return (
            self.product_repository.exists_by_slug(
                slug,
            )
        )