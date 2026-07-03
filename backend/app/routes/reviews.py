from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.store.review_service import ReviewService
from app.schemas.review import ProductReviewCreateSchema, ProductReviewUpdateSchema, ProductReviewResponseSchema
from app.core.dependencies import get_current_user
from app.models.store.customer import Customer
from typing import List, Optional

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/product/{product_public_id}", response_model=List[ProductReviewResponseSchema])
async def get_product_reviews(
    product_public_id: str,
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get all reviews for a product."""
    service = ReviewService(db)
    reviews = await service.get_product_reviews(product_public_id, limit)
    return reviews


@router.post("/product/{product_public_id}", response_model=ProductReviewResponseSchema)
async def create_review(
    product_public_id: str,
    data: ProductReviewCreateSchema,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a review for a product."""
    service = ReviewService(db)
    try:
        review = await service.create(current_user.id, product_public_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return review


@router.put("/{public_id}", response_model=ProductReviewResponseSchema)
async def update_review(
    public_id: str,
    data: ProductReviewUpdateSchema,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update an existing review."""
    service = ReviewService(db)
    try:
        review = await service.update(current_user.id, public_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return review


@router.delete("/{public_id}")
async def delete_review(
    public_id: str,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a review."""
    service = ReviewService(db)
    try:
        await service.delete(current_user.id, public_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Review deleted"}