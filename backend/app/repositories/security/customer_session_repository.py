from __future__ import annotations


from datetime import datetime
from uuid import UUID



from sqlalchemy import (
    select,
    update,
)

from sqlalchemy.orm import Session

from app.models.security.customer_session import (
    CustomerSession,
)

from app.repositories.base import (
    BaseRepository,
)


class CustomerSessionRepository(
    BaseRepository[CustomerSession],
):
    """
    Repository responsible for customer
    session persistence.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

    # ---------------------------------------------------------
    # Create
    # ---------------------------------------------------------

    def create(
        self,
        session: CustomerSession,
    ) -> CustomerSession:

        return self.create(session)

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    def get_by_public_id(
        self,
        public_id: str,
    ) -> CustomerSession | None:

        statement = (
            select(CustomerSession)
            .where(
                CustomerSession.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_refresh_token_hash(
        self,
        refresh_token_hash: str,
    ) -> CustomerSession | None:

        statement = (
            select(CustomerSession)
            .where(
                CustomerSession.refresh_token_hash
                == refresh_token_hash,
            )
        )

        return self.db.scalar(statement)

    def get_active_session(
        self,
        customer_id: UUID,
        refresh_token_hash: str,
    ) -> CustomerSession | None:

        statement = (
            select(CustomerSession)
            .where(
                CustomerSession.customer_id == customer_id,
            )
            .where(
                CustomerSession.refresh_token_hash
                == refresh_token_hash,
            )
            .where(
                CustomerSession.revoked_at.is_(None),
            )
        )

        return self.db.scalar(statement)

    def get_customer_sessions(
        self,
        customer_id: UUID,
    ) -> list[CustomerSession]:

        statement = (
            select(CustomerSession)
            .where(
                CustomerSession.customer_id == customer_id,
            )
            .where(
                CustomerSession.revoked_at.is_(None),
            )
            .order_by(
                CustomerSession.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    # ---------------------------------------------------------
    # Persistence
    # ---------------------------------------------------------

    def save(
        self,
        session: CustomerSession,
    ) -> CustomerSession:

        self.flush()

        self.refresh(session)

        return session

    # ---------------------------------------------------------
    # Bulk Operations
    # ---------------------------------------------------------

    def revoke_all_sessions(
        self,
        customer_id: UUID,
        revoked_at,
    ) -> None:

        statement = (
            update(CustomerSession)
            .where(
                CustomerSession.customer_id
                == customer_id,
            )
            .where(
                CustomerSession.revoked_at.is_(None),
            )
            .values(
                revoked_at=revoked_at,
            )
        )

        self.db.execute(statement)

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def remove(
        self,
        session: CustomerSession,
    ) -> None:

        self.delete(session)
        
    def revoke(
        self,
        session: CustomerSession,
        revoked_at: datetime,
    ) -> CustomerSession:

        session.revoked_at = revoked_at

        return self.save(session)