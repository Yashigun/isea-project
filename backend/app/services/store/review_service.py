from __future__ import annotations

from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.store.review_repository import ReviewRepository
from app.repositories.store.product_repository import ProductRepository

from app.models.store.review import (
    ProductReview,
    ProductReviewImage,
)

from app.schemas.review import (
    ProductReviewCreateSchema,
    ProductReviewUpdateSchema,
)

from app.services.store.cloudinary_service import CloudinaryService

from app.validators.product import (
    validate_original_filename,
    validate_mime_type,
    validate_file_size,
)


class ReviewService:

    MAX_REVIEW_IMAGES = 2

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

        self.repo = ReviewRepository(db)

        self.product_repo = ProductRepository(db)

    # ---------------------------------------------------------
    # READ
    # ---------------------------------------------------------

    async def get_product_reviews(
        self,
        product_public_id: str,
        limit: int,
    ) -> List[ProductReview]:

        product = await self.product_repo.get_active_by_public_id(
            product_public_id
        )

        if not product:
            return []

        reviews = await self.repo.get_product_reviews(
            product.id
        )

        return reviews[:limit] if limit else reviews

    async def list_recent(
        self,
        limit: int | None = None,
    ) -> List[ProductReview]:

        return await self.repo.list_recent(limit)

    # ---------------------------------------------------------
    # CREATE REVIEW
    # ---------------------------------------------------------

    async def create(
        self,
        customer_id: UUID,
        product_public_id: str,
        data: ProductReviewCreateSchema,
    ) -> ProductReview:

        product = await self.product_repo.get_active_by_public_id(
            product_public_id
        )

        if not product:
            raise ValueError("Product not found")

        existing = await self.repo.get_customer_review(
            customer_id,
            product.id,
        )

        if existing:
            existing.rating = data.rating
            existing.title = data.title
            existing.review = data.review

            await self.repo.save(existing)

            await self.db.commit()

            updated = await self.repo.get_by_public_id(
                existing.public_id
            )

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

        created = await self.repo.get_by_public_id(
            review.public_id
        )

        return created or review

    # ---------------------------------------------------------
    # UPLOAD REVIEW IMAGES
    # ---------------------------------------------------------

    async def upload_images(
        self,
        customer_id: UUID,
        review_public_id: str,
        files: list,
    ) -> ProductReview:

        review = await self.repo.get_by_public_id(
            review_public_id
        )

        if (
            not review
            or review.customer_id != customer_id
        ):
            raise ValueError("Review not found")

        if not files:
            return review

        if (
            len(review.images) + len(files)
            > self.MAX_REVIEW_IMAGES
        ):
            raise ValueError(
                f"A review can contain a maximum of "
                f"{self.MAX_REVIEW_IMAGES} images."
            )

        uploaded_cloudinary_ids: list[str] = []

        try:

            for file in files:

                original_filename = validate_original_filename(
                    file.filename or ""
                )

                mime_type = validate_mime_type(
                    file.content_type or ""
                )

                file_bytes = await file.read()

                file_size = validate_file_size(
                    len(file_bytes)
                )

                upload_result = (
                    await CloudinaryService.upload_image(
                        file_bytes=file_bytes,
                        filename=original_filename,
                        folder="reviews",
                    )
                )

                cloudinary_public_id = upload_result[
                    "public_id"
                ]

                uploaded_cloudinary_ids.append(
                    cloudinary_public_id
                )

                review_image = ProductReviewImage(
                    review_id=review.id,
                    image_url=upload_result["secure_url"],
                    cloudinary_public_id=cloudinary_public_id,
                    original_filename=original_filename,
                    mime_type=mime_type,
                    file_size=file_size,
                )

                self.db.add(review_image)

            await self.db.commit()

        except Exception:

            await self.db.rollback()

            # Prevent orphaned Cloudinary images.
            for cloudinary_public_id in uploaded_cloudinary_ids:
                try:
                    await CloudinaryService.delete_image(
                        cloudinary_public_id
                    )
                except Exception:
                    # Do not hide the original exception.
                    pass

            raise

        updated = await self.repo.get_by_public_id(
            review_public_id
        )

        return updated or review

    # ---------------------------------------------------------
    # UPDATE REVIEW
    # ---------------------------------------------------------

    async def update(
        self,
        customer_id: UUID,
        public_id: str,
        data: ProductReviewUpdateSchema,
    ) -> ProductReview:

        review = await self.repo.get_by_public_id(
            public_id
        )

        if (
            not review
            or review.customer_id != customer_id
        ):
            raise ValueError("Review not found")

        if data.rating is not None:
            review.rating = data.rating

        if data.title is not None:
            review.title = data.title

        if data.review is not None:
            review.review = data.review

        await self.repo.save(review)

        await self.db.commit()

        updated = await self.repo.get_by_public_id(
            public_id
        )

        return updated or review

    # ---------------------------------------------------------
    # ADMIN DELETE REVIEW
    # ---------------------------------------------------------

    async def delete(
        self,
        public_id: str,
    ) -> None:

        review = await self.repo.get_by_public_id(
            public_id
        )

        if not review:
            raise ValueError("Review not found")

        cloudinary_public_ids = [
            image.cloudinary_public_id
            for image in review.images
        ]

        # Delete database review first.
        # ProductReviewImage rows are deleted through cascade.
        await self.repo.remove(review)

        await self.db.commit()

        # Then clean up Cloudinary.
        for cloudinary_public_id in cloudinary_public_ids:

            try:
                await CloudinaryService.delete_image(
                    cloudinary_public_id
                )

            except Exception:
                # Review is already deleted from DB.
                # Cloudinary cleanup failure should be logged
                # and retried later in a production system.
                pass