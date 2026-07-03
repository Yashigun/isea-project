from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store.customer import Customer
from app.repositories.base import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    """
    Repository responsible only for customer database access.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[Customer]:
        return Customer

    # ---------------------------------------------------------
    # Create
    # ---------------------------------------------------------

    async def create(self, customer: Customer) -> Customer:
        self.db.add(customer)
        await self.db.flush()
        return customer

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(self, customer_id: UUID) -> Customer | None:
        stmt = select(Customer).where(Customer.id == customer_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, public_id: str) -> Customer | None:
        stmt = select(Customer).where(Customer.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Customer | None:
        stmt = select(Customer).where(Customer.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_email(self, email: str) -> bool:
        stmt = select(Customer.id).where(Customer.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    # ---------------------------------------------------------
    # Persistence
    # ---------------------------------------------------------

    async def save(self, customer: Customer) -> Customer:
        await self.db.flush()
        await self.db.refresh(customer)
        return customer

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    async def remove(self, customer: Customer) -> None:
        await self.db.delete(customer)
        await self.db.flush()

    async def update_last_login(self, customer: Customer, logged_in_at: datetime) -> Customer:
        customer.last_login_at = logged_in_at
        await self.db.flush()
        await self.db.refresh(customer)
        return customer