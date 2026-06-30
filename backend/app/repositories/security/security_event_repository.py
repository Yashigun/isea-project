from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    func,
    select,
)

from sqlalchemy.orm import Session

from app.models.security.security_event import (
    SecurityEvent,
    SecurityEventSeverity,
    SecurityEventType,
)

from app.repositories.base import (
    BaseRepository,
)


class SecurityEventRepository(
    BaseRepository[SecurityEvent],
):
    """
    Repository responsible for security
    event database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    def get_by_id(
        self,
        event_id: UUID,
    ) -> SecurityEvent | None:

        statement = (
            select(SecurityEvent)
            .where(
                SecurityEvent.id == event_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_public_id(
        self,
        public_id: str,
    ) -> SecurityEvent | None:

        statement = (
            select(SecurityEvent)
            .where(
                SecurityEvent.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_customer_events(
        self,
        customer_id: UUID,
        limit: int = 100,
    ) -> list[SecurityEvent]:

        statement = (
            select(SecurityEvent)
            .where(
                SecurityEvent.customer_id == customer_id,
            )
            .order_by(
                SecurityEvent.created_at.desc(),
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(statement)
        )

    def get_by_ip(
        self,
        ip_address: str,
        limit: int = 100,
    ) -> list[SecurityEvent]:

        statement = (
            select(SecurityEvent)
            .where(
                SecurityEvent.ip_address == ip_address,
            )
            .order_by(
                SecurityEvent.created_at.desc(),
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(statement)
        )

    def get_by_type(
        self,
        event_type: SecurityEventType,
        limit: int = 100,
    ) -> list[SecurityEvent]:

        statement = (
            select(SecurityEvent)
            .where(
                SecurityEvent.event_type == event_type,
            )
            .order_by(
                SecurityEvent.created_at.desc(),
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(statement)
        )

    def get_by_severity(
        self,
        severity: SecurityEventSeverity,
        limit: int = 100,
    ) -> list[SecurityEvent]:

        statement = (
            select(SecurityEvent)
            .where(
                SecurityEvent.severity == severity,
            )
            .order_by(
                SecurityEvent.created_at.desc(),
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(statement)
        )

    def get_between(
        self,
        start_time: datetime,
        end_time: datetime,
    ) -> list[SecurityEvent]:

        statement = (
            select(SecurityEvent)
            .where(
                SecurityEvent.created_at >= start_time,
            )
            .where(
                SecurityEvent.created_at <= end_time,
            )
            .order_by(
                SecurityEvent.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def count_events(
        self,
    ) -> int:

        statement = (
            select(
                func.count(
                    SecurityEvent.id,
                )
            )
        )

        return self.db.scalar(statement) or 0

    def count_by_type(
        self,
        event_type: SecurityEventType,
    ) -> int:

        statement = (
            select(
                func.count(
                    SecurityEvent.id,
                )
            )
            .where(
                SecurityEvent.event_type == event_type,
            )
        )

        return self.db.scalar(statement) or 0

    def count_by_severity(
        self,
        severity: SecurityEventSeverity,
    ) -> int:

        statement = (
            select(
                func.count(
                    SecurityEvent.id,
                )
            )
            .where(
                SecurityEvent.severity == severity,
            )
        )

        return self.db.scalar(statement) or 0

    def count_ip_events(
        self,
        ip_address: str,
        since: datetime,
    ) -> int:

        statement = (
            select(
                func.count(
                    SecurityEvent.id,
                )
            )
            .where(
                SecurityEvent.ip_address == ip_address,
            )
            .where(
                SecurityEvent.created_at >= since,
            )
        )

        return self.db.scalar(statement) or 0