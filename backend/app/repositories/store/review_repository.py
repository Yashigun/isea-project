from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.store.review import ProductReview
from app.repositories.base import BaseRepository


class ReviewRepository(BaseRepository[ProductReview]):
    """
    Repository responsible for product review database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[ProductReview]:
        return ProductReview

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(self, review_id: UUID) -> ProductReview | None:
        stmt = select(ProductReview).where(ProductReview.id == review_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, public_id: str) -> ProductReview | None:
        stmt = select(ProductReview).where(ProductReview.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_customer_review(self, customer_id: UUID, product_id: UUID) -> ProductReview | None:
        stmt = (
            select(ProductReview)
            .where(ProductReview.customer_id == customer_id)
            .where(ProductReview.product_id == product_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_product_reviews(self, product_id: UUID) -> list[ProductReview]:
        stmt = (
            select(ProductReview)
            .options(selectinload(ProductReview.customer))
            .where(ProductReview.product_id == product_id)
            .order_by(ProductReview.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_customer_reviews(self, customer_id: UUID) -> list[ProductReview]:
        stmt = (
            select(ProductReview)
            .options(selectinload(ProductReview.product))
            .where(ProductReview.customer_id == customer_id)
            .order_by(ProductReview.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    async def count_product_reviews(self, product_id: UUID) -> int:
        stmt = select(func.count(ProductReview.id)).where(ProductReview.product_id == product_id)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_average_rating(self, product_id: UUID) -> float:
        stmt = select(func.avg(ProductReview.rating)).where(ProductReview.product_id == product_id)
        result = await self.db.execute(stmt)
        avg = result.scalar()
        if avg is None:
            return 0.0
        return round(float(avg), 2)

    async def rating_breakdown(self, product_id: UUID) -> dict[int, int]:
        stmt = (
            select(ProductReview.rating, func.count(ProductReview.id))
            .where(ProductReview.product_id == product_id)
            .group_by(ProductReview.rating)
        )
        result = await self.db.execute(stmt)
        rows = result.all()
        breakdown = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for rating, count in rows:
            breakdown[rating] = count
        return breakdown