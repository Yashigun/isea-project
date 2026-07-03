from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.store.wishlist_service import WishlistService
from app.schemas.product import ProductSummarySchema
from app.core.dependencies import get_current_user
from app.models.store.customer import Customer
from typing import List

router = APIRouter(prefix="/wishlist", tags=["wishlist"])


@router.get("/", response_model=List[ProductSummarySchema])
async def get_wishlist(
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the current user's wishlist."""
    service = WishlistService(db)
    items = await service.get_customer_wishlist(current_user.id)
    # Return product summaries
    return [item.product for item in items]


@router.post("/{product_public_id}")
async def add_to_wishlist(
    product_public_id: str,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add a product to the wishlist."""
    service = WishlistService(db)
    try:
        await service.add_item(current_user.id, product_public_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Product added to wishlist"}


@router.delete("/{product_public_id}")
async def remove_from_wishlist(
    product_public_id: str,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Remove a product from the wishlist."""
    service = WishlistService(db)
    try:
        await service.remove_item(current_user.id, product_public_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Product removed from wishlist"}