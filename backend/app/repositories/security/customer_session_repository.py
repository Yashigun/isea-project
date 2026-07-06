from __future__ import annotations

from datetime import datetime, timezone
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
            .where(
                CustomerSession.id == session_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_public_id(
        self,
        public_id: str,
    ) -> Optional[CustomerSession]:

        stmt = (
            select(CustomerSession)
            .where(
                CustomerSession.public_id == public_id
            )
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

    # ---------------------------------------------------------
    # Admin Session Listing
    # ---------------------------------------------------------

    async def list_all_sessions(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[CustomerSession], int]:

        count_stmt = select(
            func.count(CustomerSession.id)
        )

        count_result = await self.db.execute(
            count_stmt
        )

        total = count_result.scalar() or 0

        stmt = (
            select(CustomerSession)
            .order_by(
                CustomerSession.created_at.desc()
            )
            .limit(limit)
            .offset(offset)
        )

        result = await self.db.execute(stmt)

        sessions = list(
            result.scalars().all()
        )

        return sessions, total

    # ---------------------------------------------------------
    # Customer Sessions
    # ---------------------------------------------------------

    async def list_customer_sessions(
        self,
        customer_id: UUID,
    ) -> list[CustomerSession]:

        stmt = (
            select(CustomerSession)
            .where(
                CustomerSession.customer_id
                == customer_id
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

        now = datetime.now(timezone.utc)

        stmt = (
            select(CustomerSession)
            .where(
                CustomerSession.customer_id
                == customer_id
            )
            .where(
                CustomerSession.revoked_at.is_(None)
            )
            .where(
                CustomerSession.expires_at > now
            )
            .order_by(
                CustomerSession.created_at.desc()
            )
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def get_active_session(
        self,
        customer_id: UUID,
        public_id: str,
    ) -> Optional[CustomerSession]:

        now = datetime.now(timezone.utc)

        stmt = (
            select(CustomerSession)
            .where(
                CustomerSession.customer_id
                == customer_id
            )
            .where(
                CustomerSession.public_id
                == public_id
            )
            .where(
                CustomerSession.revoked_at.is_(None)
            )
            .where(
                CustomerSession.expires_at > now
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    async def count_active_sessions(
        self,
        customer_id: UUID | None = None,
    ) -> int:

        now = datetime.now(timezone.utc)

        stmt = (
            select(
                func.count(CustomerSession.id)
            )
            .where(
                CustomerSession.revoked_at.is_(None)
            )
            .where(
                CustomerSession.expires_at > now
            )
        )

        if customer_id is not None:
            stmt = stmt.where(
                CustomerSession.customer_id
                == customer_id
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

        session.revoked_at = datetime.now(
            timezone.utc
        )

        await self.db.flush()

        return session

    async def deactivate_all(
        self,
        customer_id: UUID,
    ) -> None:

        sessions = await self.list_active_sessions(
            customer_id
        )

        revoked_at = datetime.now(timezone.utc)

        for session in sessions:
            session.revoked_at = revoked_at

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