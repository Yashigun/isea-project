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

from app.models.security.request_log import (
    RequestLog,
)

from app.repositories.base import (
    BaseRepository,
)


class RequestLogRepository(
    BaseRepository[RequestLog],
):
    """
    Repository responsible for HTTP request
    logging and forensic queries.
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
        request_log_id: UUID,
    ) -> RequestLog | None:

        statement = (
            select(RequestLog)
            .where(
                RequestLog.id == request_log_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_public_id(
        self,
        public_id: str,
    ) -> RequestLog | None:

        statement = (
            select(RequestLog)
            .where(
                RequestLog.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_recent(
        self,
        limit: int = 100,
    ) -> list[RequestLog]:

        statement = (
            select(RequestLog)
            .order_by(
                RequestLog.created_at.desc(),
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(statement)
        )

    def get_customer_requests(
        self,
        customer_id: UUID,
        limit: int = 100,
    ) -> list[RequestLog]:

        statement = (
            select(RequestLog)
            .where(
                RequestLog.customer_id == customer_id,
            )
            .order_by(
                RequestLog.created_at.desc(),
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(statement)
        )

    def get_ip_requests(
        self,
        ip_address: str,
        limit: int = 100,
    ) -> list[RequestLog]:

        statement = (
            select(RequestLog)
            .where(
                RequestLog.ip_address == ip_address,
            )
            .order_by(
                RequestLog.created_at.desc(),
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
    ) -> list[RequestLog]:

        statement = (
            select(RequestLog)
            .where(
                RequestLog.created_at >= start_time,
            )
            .where(
                RequestLog.created_at <= end_time,
            )
            .order_by(
                RequestLog.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def get_by_method(
        self,
        method: str,
        limit: int = 100,
    ) -> list[RequestLog]:

        statement = (
            select(RequestLog)
            .where(
                RequestLog.request_method == method,
            )
            .order_by(
                RequestLog.created_at.desc(),
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(statement)
        )

    def get_by_status_code(
        self,
        status_code: int,
        limit: int = 100,
    ) -> list[RequestLog]:

        statement = (
            select(RequestLog)
            .where(
                RequestLog.response_status == status_code,
            )
            .order_by(
                RequestLog.created_at.desc(),
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(statement)
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def count_requests(
        self,
    ) -> int:

        statement = (
            select(
                func.count(
                    RequestLog.id,
                )
            )
        )

        return self.db.scalar(statement) or 0

    def count_ip_requests(
        self,
        ip_address: str,
        since: datetime,
    ) -> int:

        statement = (
            select(
                func.count(
                    RequestLog.id,
                )
            )
            .where(
                RequestLog.ip_address == ip_address,
            )
            .where(
                RequestLog.created_at >= since,
            )
        )

        return self.db.scalar(statement) or 0

    def count_customer_requests(
        self,
        customer_id: UUID,
        since: datetime,
    ) -> int:

        statement = (
            select(
                func.count(
                    RequestLog.id,
                )
            )
            .where(
                RequestLog.customer_id == customer_id,
            )
            .where(
                RequestLog.created_at >= since,
            )
        )

        return self.db.scalar(statement) or 0

    def count_status_code(
        self,
        status_code: int,
        since: datetime,
    ) -> int:

        statement = (
            select(
                func.count(
                    RequestLog.id,
                )
            )
            .where(
                RequestLog.response_status == status_code,
            )
            .where(
                RequestLog.created_at >= since,
            )
        )

        return self.db.scalar(statement) or 0