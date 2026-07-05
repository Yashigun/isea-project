from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.dependencies import get_current_admin
from app.services.store.order_service import OrderService
from app.models.store.order import OrderStatus

router = APIRouter(
    prefix="/admin/orders",
    tags=["admin-orders"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("/")
async def list_orders(
    db: AsyncSession = Depends(get_db),
):
    service = OrderService(db)

    return await service.get_all_orders()


@router.get("/{public_id}")
async def get_order(
    public_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = OrderService(db)

    try:
        return await service.get_admin_order(public_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.patch("/{public_id}/status")
async def update_status(
    public_id: str,
    status: OrderStatus,
    db: AsyncSession = Depends(get_db),
):
    service = OrderService(db)

    try:
        return await service.update_status(
            public_id,
            status,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )