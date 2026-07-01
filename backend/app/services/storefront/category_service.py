from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.store.category_repository import (
    CategoryRepository,
)

from app.schemas.category import (
    CategoryResponseSchema,
)

from app.services.base import BaseService


class CategoryService(BaseService):
    """
    Customer-facing category service.
    """

    def __init__( self, db: Session ) -> None:

        super().__init__(db)

        self.category_repository = (
            CategoryRepository(db)
        )

    # ---------------------------------------------------------
    # Public Categories
    # ---------------------------------------------------------

    def list_categories( self ) -> list[CategoryResponseSchema]:

        categories = (
            self.category_repository.get_active_categories()
        )

        return self.to_schema_list(
            categories,
            CategoryResponseSchema,
        )

    def get_category_by_slug( self, slug: str ) -> CategoryResponseSchema | None:

        category = (
            self.category_repository.get_active_by_slug(
                slug,
            )
        )

        if category is None:
            return None

        return self.to_schema(
            category,
            CategoryResponseSchema,
        )

    def get_category_by_public_id( self, public_id: str ) -> CategoryResponseSchema | None:

        category = (
            self.category_repository.get_active_by_public_id(
                public_id,
            )
        )

        if category is None:
            return None

        return self.to_schema(
            category,
            CategoryResponseSchema,
        )

    def category_exists( self, slug: str ) -> bool:

        return (
            self.category_repository.exists_by_slug(
                slug,
            )
        )
    