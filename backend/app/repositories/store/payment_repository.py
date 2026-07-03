from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store.payment import Payment, PaymentStatus
from app.repositories.base import BaseRepository


class PaymentRepository(BaseRepository[Payment]):
    """
    Repository responsible for payment database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[Payment]:
        return Payment

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(self, payment_id: UUID) -> Payment | None:
        stmt = select(Payment).where(Payment.id == payment_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, public_id: str) -> Payment | None:
        stmt = select(Payment).where(Payment.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_order_id(self, order_id: UUID) -> Payment | None:
        stmt = select(Payment).where(Payment.order_id == order_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_transaction_reference(self, transaction_reference: str) -> Payment | None:
        stmt = select(Payment).where(Payment.transaction_reference == transaction_reference)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_gateway_reference(self, gateway_name: str, transaction_reference: str) -> Payment | None:
        stmt = (
            select(Payment)
            .where(Payment.gateway_name == gateway_name)
            .where(Payment.transaction_reference == transaction_reference)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_status(self, payment_status: PaymentStatus) -> list[Payment]:
        stmt = (
            select(Payment)
            .where(Payment.payment_status == payment_status)
            .order_by(Payment.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def payment_exists(self, transaction_reference: str) -> bool:
        stmt = select(Payment.id).where(Payment.transaction_reference == transaction_reference)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None