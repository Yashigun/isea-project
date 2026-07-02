from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    func,
    select,
)

from sqlalchemy.orm import Session

from app.models.security.login_attempt import LoginAttempt

from app.repositories.base import BaseRepository


class LoginAttemptRepository(
    BaseRepository[LoginAttempt],
):
    """
    Repository responsible for login attempt
    database operations.
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
        attempt: LoginAttempt,
    ) -> LoginAttempt:
        """
        Persist a login attempt.
        """

        return self.add(attempt)
    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    def get_by_id(
        self,
        attempt_id: UUID,
    ) -> LoginAttempt | None:

        statement = (
            select(LoginAttempt)
            .where(
                LoginAttempt.id == attempt_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_public_id(
        self,
        public_id: str,
    ) -> LoginAttempt | None:

        statement = (
            select(LoginAttempt)
            .where(
                LoginAttempt.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_customer_attempts(
        self,
        customer_id: UUID,
        limit: int = 20,
    ) -> list[LoginAttempt]:

        statement = (
            select(LoginAttempt)
            .where(
                LoginAttempt.customer_id == customer_id,
            )
            .order_by(
                LoginAttempt.created_at.desc(),
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(statement)
        )

    def get_ip_attempts(
        self,
        ip_address: str,
        limit: int = 100,
    ) -> list[LoginAttempt]:

        statement = (
            select(LoginAttempt)
            .where(
                LoginAttempt.ip_address == ip_address,
            )
            .order_by(
                LoginAttempt.created_at.desc(),
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(statement)
        )

    def get_recent_failures(
        self,
        since: datetime,
    ) -> list[LoginAttempt]:

        statement = (
            select(LoginAttempt)
            .where(
                LoginAttempt.success.is_(False),
            )
            .where(
                LoginAttempt.created_at >= since,
            )
            .order_by(
                LoginAttempt.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def count_recent_failures(
        self,
        ip_address: str,
        since: datetime,
    ) -> int:

        statement = (
            select(
                func.count(LoginAttempt.id),
            )
            .where(
                LoginAttempt.ip_address == ip_address,
            )
            .where(
                LoginAttempt.success.is_(False),
            )
            .where(
                LoginAttempt.created_at >= since,
            )
        )

        return self.db.scalar(statement) or 0

    def count_customer_failures(
        self,
        customer_id: UUID,
        since: datetime,
    ) -> int:

        statement = (
            select(
                func.count(LoginAttempt.id),
            )
            .where(
                LoginAttempt.customer_id == customer_id,
            )
            .where(
                LoginAttempt.success.is_(False),
            )
            .where(
                LoginAttempt.created_at >= since,
            )
        )

        return self.db.scalar(statement) or 0

    def count_ip_attempts(
        self,
        ip_address: str,
        since: datetime,
    ) -> int:

        statement = (
            select(
                func.count(LoginAttempt.id),
            )
            .where(
                LoginAttempt.ip_address == ip_address,
            )
            .where(
                LoginAttempt.created_at >= since,
            )
        )

        return self.db.scalar(statement) or 0