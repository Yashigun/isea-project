from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.security.customer_session import CustomerSession
from app.repositories.base import BaseRepository


class CustomerSessionRepository(BaseRepository[CustomerSession]):
    """
    Repository responsible for customer session persistence.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    def _get_model(self) -> type[CustomerSession]:
        return CustomerSession

    # ---------------------------------------------------------
    # Create
    # ---------------------------------------------------------

    async def create(self, session: CustomerSession) -> CustomerSession:
        self.db.add(session)
        await self.db.flush()
        return session

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_public_id(self, public_id: str) -> CustomerSession | None:
        stmt = select(CustomerSession).where(CustomerSession.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_refresh_token_hash(self, refresh_token_hash: str) -> CustomerSession | None:
        stmt = select(CustomerSession).where(CustomerSession.refresh_token_hash == refresh_token_hash)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_session(self, customer_id: UUID, refresh_token_hash: str) -> CustomerSession | None:
        stmt = (
            select(CustomerSession)
            .where(CustomerSession.customer_id == customer_id)
            .where(CustomerSession.refresh_token_hash == refresh_token_hash)
            .where(CustomerSession.revoked_at.is_(None))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_customer_sessions(self, customer_id: UUID) -> list[CustomerSession]:
        stmt = (
            select(CustomerSession)
            .where(CustomerSession.customer_id == customer_id)
            .where(CustomerSession.revoked_at.is_(None))
            .order_by(CustomerSession.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # ---------------------------------------------------------
    # Persistence
    # ---------------------------------------------------------

    async def save(self, session: CustomerSession) -> CustomerSession:
        await self.db.flush()
        await self.db.refresh(session)
        return session

    # ---------------------------------------------------------
    # Bulk Operations
    # ---------------------------------------------------------

    async def revoke_all_sessions(self, customer_id: UUID, revoked_at: datetime) -> None:
        stmt = (
            update(CustomerSession)
            .where(CustomerSession.customer_id == customer_id)
            .where(CustomerSession.revoked_at.is_(None))
            .values(revoked_at=revoked_at)
        )
        await self.db.execute(stmt)
        await self.db.flush()

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    async def remove(self, session: CustomerSession) -> None:
        await self.db.delete(session)
        await self.db.flush()

    async def revoke(self, session: CustomerSession, revoked_at: datetime) -> CustomerSession:
        session.revoked_at = revoked_at
        await self.db.flush()
        await self.db.refresh(session)
        return session