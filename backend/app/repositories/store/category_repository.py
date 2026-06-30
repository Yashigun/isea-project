from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.store.category import (
    Category,
)

from app.repositories.base import (
    BaseRepository,
)


class CategoryRepository(
    BaseRepository[Category],
):
    """
    Repository responsible for category
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
        category_id,
    ) -> Category | None:

        statement = (
            select(Category)
            .where(
                Category.id == category_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_public_id(
        self,
        public_id: str,
    ) -> Category | None:

        statement = (
            select(Category)
            .where(
                Category.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_slug(
        self,
        slug: str,
    ) -> Category | None:

        statement = (
            select(Category)
            .where(
                Category.slug == slug,
            )
        )

        return self.db.scalar(statement)

    def get_by_name(
        self,
        name: str,
    ) -> Category | None:

        statement = (
            select(Category)
            .where(
                Category.name == name,
            )
        )

        return self.db.scalar(statement)

    def exists_by_slug(
        self,
        slug: str,
    ) -> bool:

        statement = (
            select(Category.id)
            .where(
                Category.slug == slug,
            )
        )

        return self.db.scalar(statement) is not None

    def exists_by_name(
        self,
        name: str,
    ) -> bool:

        statement = (
            select(Category.id)
            .where(
                Category.name == name,
            )
        )

        return self.db.scalar(statement) is not None

    def get_active_categories(
        self,
    ) -> list[Category]:

        statement = (
            select(Category)
            .where(
                Category.is_active.is_(True),
            )
            .order_by(
                Category.name.asc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def get_all(
        self,
    ) -> list[Category]:

        statement = (
            select(Category)
            .order_by(
                Category.name.asc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )