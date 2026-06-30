from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    func,
    select,
)

from sqlalchemy.orm import (
    Session,
)

from app.models.security.audit_log import AuditLog
from app.models.security.audit_log import AuditAction

from app.repositories.base import BaseRepository


class AuditLogRepository(
    BaseRepository[AuditLog],
):
    """
    Repository responsible for audit log
    database operations.
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
        audit_log_id: UUID,
    ) -> AuditLog | None:

        statement = (
            select(AuditLog)
            .where(
                AuditLog.id == audit_log_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_public_id(
        self,
        public_id: str,
    ) -> AuditLog | None:

        statement = (
            select(AuditLog)
            .where(
                AuditLog.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_customer_logs(
        self,
        customer_id: UUID,
        limit: int = 100,
    ) -> list[AuditLog]:

        statement = (
            select(AuditLog)
            .where(
                AuditLog.customer_id == customer_id,
            )
            .order_by(
                AuditLog.created_at.desc(),
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(statement)
        )

    def get_by_action(
        self,
        action: AuditAction,
        limit: int = 100,
    ) -> list[AuditLog]:

        statement = (
            select(AuditLog)
            .where(
                AuditLog.action == action,
            )
            .order_by(
                AuditLog.created_at.desc(),
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
    ) -> list[AuditLog]:

        statement = (
            select(AuditLog)
            .where(
                AuditLog.created_at >= start_time,
            )
            .where(
                AuditLog.created_at <= end_time,
            )
            .order_by(
                AuditLog.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def count_logs(
        self,
    ) -> int:

        statement = (
            select(
                func.count(
                    AuditLog.id,
                )
            )
        )

        return self.db.scalar(statement) or 0

    def count_customer_logs(
        self,
        customer_id: UUID,
    ) -> int:

        statement = (
            select(
                func.count(
                    AuditLog.id,
                )
            )
            .where(
                AuditLog.customer_id == customer_id,
            )
        )

        return self.db.scalar(statement) or 0

    def count_action(
        self,
        action: AuditAction,
    ) -> int:

        statement = (
            select(
                func.count(
                    AuditLog.id,
                )
            )
            .where(
                AuditLog.action == action,
            )
        )

        return self.db.scalar(statement) or 0