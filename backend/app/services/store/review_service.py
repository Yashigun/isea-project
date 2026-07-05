from __future__ import annotations

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.store.review_repository import ReviewRepository
from app.repositories.store.product_repository import ProductRepository
from app.models.store.review import ProductReview
from app.schemas.review import ProductReviewCreateSchema, ProductReviewUpdateSchema


class ReviewService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ReviewRepository(db)
        self.product_repo = ProductRepository(db)

    async def get_product_reviews(self, product_public_id: str, limit: int) -> List[ProductReview]:
        product = await self.product_repo.get_active_by_public_id(product_public_id)
        if not product:
            return []
        reviews = await self.repo.get_product_reviews(product.id)
        return reviews[:limit] if limit else reviews

    async def list_recent(self, limit: int | None = None) -> List[ProductReview]:
        return await self.repo.list_recent(limit)

    async def create(self, customer_id: UUID, product_public_id: str, data: ProductReviewCreateSchema) -> ProductReview:
        product = await self.product_repo.get_active_by_public_id(product_public_id)
        if not product:
            raise ValueError("Product not found")
        existing = await self.repo.get_customer_review(customer_id, product.id)
        if existing:
            existing.rating = data.rating
            existing.title = data.title
            existing.review = data.review
            await self.repo.save(existing)
            await self.db.commit()
            updated = await self.repo.get_by_public_id(existing.public_id)
            return updated or existing
        review = ProductReview(
            customer_id=customer_id,
            product_id=product.id,
            rating=data.rating,
            title=data.title,
            review=data.review,
        )
        await self.repo.create(review)
        await self.db.commit()
        created = await self.repo.get_by_public_id(review.public_id)
        return created or review

    async def update(self, customer_id: UUID, public_id: str, data: ProductReviewUpdateSchema) -> ProductReview:
        review = await self.repo.get_by_public_id(public_id)
        if not review or review.customer_id != customer_id:
            raise ValueError("Review not found")
        if data.rating is not None:
            review.rating = data.rating
        if data.title is not None:
            review.title = data.title
        if data.review is not None:
            review.review = data.review
        await self.repo.save(review)
        await self.db.commit()
        updated = await self.repo.get_by_public_id(public_id)
        return updated or review

    async def delete(self, customer_id: UUID, public_id: str) -> None:
        review = await self.repo.get_by_public_id(public_id)
        if not review or review.customer_id != customer_id:
            raise ValueError("Review not found")
        await self.repo.remove(review)
        await self.db.commit()
