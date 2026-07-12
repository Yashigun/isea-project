from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.store.order_service import OrderService
from app.schemas.order import OrderCreateSchema, OrderResponseSchema, OrderSummarySchema
from app.core.dependencies import get_current_user
from app.models.store.customer import Customer
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=List[OrderSummarySchema])
async def list_orders(
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all orders for the current user."""
    service = OrderService(db)
    orders = await service.get_customer_orders(current_user.id)
    return orders


@router.get("/{public_id}", response_model=OrderResponseSchema)
async def get_order(
    public_id: str,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific order by public ID."""
    service = OrderService(db)
    order = await service.get_customer_order(current_user.id, public_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/", response_model=OrderResponseSchema)
async def create_order(
    data: OrderCreateSchema,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new order from the current cart."""
    service = OrderService(db)
    try:
        order = await service.create_order(
            customer_id=current_user.id,
            address_public_id=data.shipping_address_public_id,
            phone_public_id=data.phone_public_id,
            payment_method=data.payment_method,
            notes=data.order_notes,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return order


@router.post("/{public_id}/cancel", response_model=OrderResponseSchema)
async def cancel_order(
    public_id: str,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Cancel an order (only if pending or confirmed)."""
    service = OrderService(db)
    try:
        order = await service.cancel_order(current_user.id, public_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return order
