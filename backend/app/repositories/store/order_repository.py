from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.store.customer import Customer
from app.models.store.payment import Payment


from app.models.store.order import Order, OrderStatus
from app.models.store.order_item import OrderItem
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """
    Repository responsible for order database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[Order]:
        return Order

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(self, order_id: UUID) -> Order | None:
        stmt = select(Order).where(Order.id == order_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, public_id: str) -> Order | None:
        stmt = select(Order).where(Order.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_order_details(self, public_id: str) -> Order | None:
        stmt = (
            select(Order)
            .options(
                selectinload(Order.items).selectinload(OrderItem.product),
                selectinload(Order.payment),
                # Shipping address is not a relationship in your model? It's stored directly.
                # If you have a separate address model, load it, otherwise skip.
            )
            .where(Order.public_id == public_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_customer_orders(self, customer_id: UUID) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.customer_id == customer_id)
            .order_by(Order.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_customer_order(self, customer_id: UUID, public_id: str) -> Order | None:
        stmt = (
            select(Order)
            .options(
                selectinload(Order.items).selectinload(OrderItem.product),
                selectinload(Order.payment),
            )
            .where(Order.customer_id == customer_id)
            .where(Order.public_id == public_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_status(self, status: OrderStatus) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.status == status)
            .order_by(Order.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_recent(self, limit: int = 20) -> list[Order]:
        stmt = select(Order).order_by(Order.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    async def count_orders(self) -> int:
        stmt = select(func.count(Order.id))
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_customer_orders(self, customer_id: UUID) -> int:
        stmt = select(func.count(Order.id)).where(Order.customer_id == customer_id)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def count_by_status(self, status: OrderStatus) -> int:
        stmt = select(func.count(Order.id)).where(Order.status == status)
        result = await self.db.execute(stmt)
        return result.scalar() or 0
    
    

    # ---------------------------------------------------------
    # Admin
    # ---------------------------------------------------------

    async def get_all_orders(self) -> list[Order]:
        stmt = (
            select(Order)
            .options(
                selectinload(Order.customer),
                selectinload(Order.items).selectinload(OrderItem.product),
                selectinload(Order.payment),
            )
            .order_by(Order.created_at.desc())
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())


    async def get_admin_order(self, public_id: str) -> Order | None:
        stmt = (
            select(Order)
            .options(
                selectinload(Order.customer),
                selectinload(Order.items).selectinload(OrderItem.product),
                selectinload(Order.payment),
            )
            .where(Order.public_id == public_id)
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()