from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    File,
    UploadFile,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db

from app.services.store.review_service import ReviewService

from app.schemas.review import (
    ProductReviewCreateSchema,
    ProductReviewUpdateSchema,
    ProductReviewResponseSchema,
)

from app.core.dependencies import get_current_user

# CHANGE THIS IMPORT TO YOUR ACTUAL ADMIN DEPENDENCY.
from app.core.dependencies import get_current_admin

from app.models.store.customer import Customer


router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)


# ---------------------------------------------------------
# LIST RECENT REVIEWS
# ---------------------------------------------------------

@router.get(
    "/",
    response_model=List[ProductReviewResponseSchema],
)
async def list_reviews(
    limit: Optional[int] = Query(
        None,
        ge=1,
        le=100,
    ),
    db: AsyncSession = Depends(get_db),
):
    service = ReviewService(db)

    return await service.list_recent(limit)


# ---------------------------------------------------------
# PRODUCT REVIEWS
# ---------------------------------------------------------

@router.get(
    "/product/{product_public_id}",
    response_model=List[ProductReviewResponseSchema],
)
async def get_product_reviews(
    product_public_id: str,
    limit: int = Query(
        10,
        ge=1,
        le=100,
    ),
    db: AsyncSession = Depends(get_db),
):
    service = ReviewService(db)

    return await service.get_product_reviews(
        product_public_id,
        limit,
    )


# ---------------------------------------------------------
# CREATE REVIEW
# ---------------------------------------------------------

@router.post(
    "/product/{product_public_id}",
    response_model=ProductReviewResponseSchema,
)
async def create_review(
    product_public_id: str,
    data: ProductReviewCreateSchema,
    current_user: Customer = Depends(
        get_current_user
    ),
    db: AsyncSession = Depends(get_db),
):
    service = ReviewService(db)

    try:

        return await service.create(
            current_user.id,
            product_public_id,
            data,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


# ---------------------------------------------------------
# UPLOAD REVIEW IMAGES
# ---------------------------------------------------------

@router.post(
    "/{public_id}/images",
    response_model=ProductReviewResponseSchema,
)
async def upload_review_images(
    public_id: str,
    files: List[UploadFile] = File(...),
    current_user: Customer = Depends(
        get_current_user
    ),
    db: AsyncSession = Depends(get_db),
):
    service = ReviewService(db)

    try:

        return await service.upload_images(
            current_user.id,
            public_id,
            files,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


# ---------------------------------------------------------
# UPDATE REVIEW
# ---------------------------------------------------------

@router.put(
    "/{public_id}",
    response_model=ProductReviewResponseSchema,
)
async def update_review(
    public_id: str,
    data: ProductReviewUpdateSchema,
    current_user: Customer = Depends(
        get_current_user
    ),
    db: AsyncSession = Depends(get_db),
):
    service = ReviewService(db)

    try:

        return await service.update(
            current_user.id,
            public_id,
            data,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


# ---------------------------------------------------------
# ADMIN DELETE REVIEW
# ---------------------------------------------------------

@router.delete(
    "/{public_id}",
    status_code=200,
)
async def delete_review(
    public_id: str,

    # Only authenticated admin reaches this endpoint.
    current_admin=Depends(get_current_admin),

    db: AsyncSession = Depends(get_db),
):
    service = ReviewService(db)

    try:

        await service.delete(public_id)

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return {
        "message": "Review deleted successfully"
    }