from __future__ import annotations

from uuid import UUID

from sqlalchemy import (
    func,
    select,
)

from sqlalchemy.orm import (
    Session,
    selectinload,
)

from app.models.store.customer import Customer
from app.models.store.product import Product
from app.models.store.product_review import ProductReview

from app.repositories.base import BaseRepository


class ReviewRepository(
    BaseRepository[ProductReview],
):
    """
    Repository responsible for product review
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
        review_id: UUID,
    ) -> ProductReview | None:

        statement = (
            select(ProductReview)
            .where(
                ProductReview.id == review_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_public_id(
        self,
        public_id: str,
    ) -> ProductReview | None:

        statement = (
            select(ProductReview)
            .where(
                ProductReview.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_customer_review(
        self,
        customer_id: UUID,
        product_id: UUID,
    ) -> ProductReview | None:

        statement = (
            select(ProductReview)
            .where(
                ProductReview.customer_id == customer_id,
            )
            .where(
                ProductReview.product_id == product_id,
            )
        )

        return self.db.scalar(statement)

    def get_product_reviews(
        self,
        product_id: UUID,
    ) -> list[ProductReview]:

        statement = (
            select(ProductReview)
            .options(
                selectinload(
                    ProductReview.customer,
                )
            )
            .where(
                ProductReview.product_id == product_id,
            )
            .order_by(
                ProductReview.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def get_customer_reviews(
        self,
        customer_id: UUID,
    ) -> list[ProductReview]:

        statement = (
            select(ProductReview)
            .options(
                selectinload(
                    ProductReview.product,
                )
            )
            .where(
                ProductReview.customer_id == customer_id,
            )
            .order_by(
                ProductReview.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def count_product_reviews(
        self,
        product_id: UUID,
    ) -> int:

        statement = (
            select(
                func.count(
                    ProductReview.id,
                )
            )
            .where(
                ProductReview.product_id == product_id,
            )
        )

        return self.db.scalar(statement) or 0

    def get_average_rating(
        self,
        product_id: UUID,
    ) -> float:

        statement = (
            select(
                func.avg(
                    ProductReview.rating,
                )
            )
            .where(
                ProductReview.product_id == product_id,
            )
        )

        average = self.db.scalar(statement)

        if average is None:
            return 0.0

        return round(
            float(average),
            2,
        )

    def rating_breakdown(
        self,
        product_id: UUID,
    ) -> dict[int, int]:
        """
        Returns:
        {
            5: 12,
            4: 8,
            3: 1,
            2: 0,
            1: 0,
        }
        """

        statement = (
            select(
                ProductReview.rating,
                func.count(
                    ProductReview.id,
                ),
            )
            .where(
                ProductReview.product_id == product_id,
            )
            .group_by(
                ProductReview.rating,
            )
        )

        rows = self.db.execute(statement).all()

        breakdown = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
        }

        for rating, count in rows:
            breakdown[rating] = count

        return breakdown