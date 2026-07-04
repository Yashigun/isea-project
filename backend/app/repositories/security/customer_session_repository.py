from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.security.customer_session import CustomerSession
from app.repositories.base import BaseRepository


class CustomerSessionRepository(BaseRepository[CustomerSession]):
    """
    Repository responsible for customer session database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        super().__init__(db)

    def _get_model(self) -> type[CustomerSession]:
        return CustomerSession

    # ---------------------------------------------------------
    # Create / Update
    # ---------------------------------------------------------

    async def create(
        self,
        session: CustomerSession,
    ) -> CustomerSession:

        self.db.add(session)

        await self.db.flush()

        return session

    async def save(
        self,
        session: CustomerSession,
    ) -> CustomerSession:

        await self.db.flush()

        return session

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(
        self,
        session_id: UUID,
    ) -> Optional[CustomerSession]:

        stmt = (
            select(CustomerSession)
            .where(CustomerSession.id == session_id)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_public_id(
        self,
        public_id: str,
    ) -> Optional[CustomerSession]:

        stmt = (
            select(CustomerSession)
            .where(CustomerSession.public_id == public_id)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_refresh_token(
        self,
        refresh_token_hash: str,
    ) -> Optional[CustomerSession]:

        stmt = (
            select(CustomerSession)
            .where(
                CustomerSession.refresh_token_hash
                == refresh_token_hash
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_active_session(
        self,
        customer_id: UUID,
        session_token: str,
    ) -> Optional[CustomerSession]:

        stmt = (
            select(CustomerSession)
            .where(
                CustomerSession.customer_id == customer_id
            )
            .where(
                CustomerSession.session_token
                == session_token
            )
            .where(
                CustomerSession.is_active.is_(True)
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def list_customer_sessions(
        self,
        customer_id: UUID,
    ) -> list[CustomerSession]:

        stmt = (
            select(CustomerSession)
            .where(
                CustomerSession.customer_id == customer_id
            )
            .order_by(
                CustomerSession.created_at.desc()
            )
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def list_active_sessions(
        self,
        customer_id: UUID,
    ) -> list[CustomerSession]:

        stmt = (
            select(CustomerSession)
            .where(
                CustomerSession.customer_id == customer_id
            )
            .where(
                CustomerSession.is_active.is_(True)
            )
            .order_by(
                CustomerSession.created_at.desc()
            )
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    async def count_active_sessions(
        self,
        customer_id: UUID,
    ) -> int:

        stmt = (
            select(func.count(CustomerSession.id))
            .where(
                CustomerSession.customer_id == customer_id
            )
            .where(
                CustomerSession.is_active.is_(True)
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar() or 0

    # ---------------------------------------------------------
    # Session Management
    # ---------------------------------------------------------

    async def deactivate(
        self,
        session: CustomerSession,
    ) -> CustomerSession:

        session.is_active = False

        await self.db.flush()

        return session

    async def deactivate_all(
        self,
        customer_id: UUID,
    ) -> None:

        sessions = await self.list_active_sessions(
            customer_id
        )

        for session in sessions:
            session.is_active = False

        await self.db.flush()

    async def delete_expired(
        self,
        now: datetime,
    ) -> int:

        stmt = (
            select(CustomerSession)
            .where(
                CustomerSession.expires_at < now
            )
        )

        result = await self.db.execute(stmt)

        sessions = result.scalars().all()

        count = len(sessions)

        for session in sessions:
            await self.db.delete(session)

        await self.db.flush()

        return count