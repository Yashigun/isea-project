from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.store.cart_service import CartService
from app.schemas.cart import CartItemCreateSchema, CartItemUpdateSchema, CartResponseSchema
from app.core.dependencies import get_current_user
from app.models.store.customer import Customer

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=CartResponseSchema)
async def get_cart(
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the current user's cart."""
    service = CartService(db)
    cart = await service.get_cart(current_user.id)
    # Convert to response schema (you'll need to implement a mapping function)
    # We'll assume CartResponseSchema accepts a Cart object
    return cart


@router.post("/items", response_model=CartResponseSchema)
async def add_to_cart(
    data: CartItemCreateSchema,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add a product to the cart."""
    service = CartService(db)
    try:
        cart = await service.add_item(
            current_user.id,
            data.product_public_id,
            data.quantity
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return cart


@router.put("/items/{product_public_id}", response_model=CartResponseSchema)
async def update_cart_item(
    product_public_id: str,
    data: CartItemUpdateSchema,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update quantity of a cart item."""
    service = CartService(db)
    try:
        cart = await service.update_quantity(
            current_user.id,
            product_public_id,
            data.quantity
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return cart


@router.delete("/items/{product_public_id}", response_model=CartResponseSchema)
async def remove_from_cart(
    product_public_id: str,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Remove a product from the cart."""
    service = CartService(db)
    try:
        cart = await service.remove_item(current_user.id, product_public_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return cart


@router.delete("/", response_model=dict)
async def clear_cart(
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Clear all items from the cart."""
    service = CartService(db)
    await service.clear_cart(current_user.id)
    return {"message": "Cart cleared"}