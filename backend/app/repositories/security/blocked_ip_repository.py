from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    and_,
    func,
    or_,
    select,
)

from sqlalchemy.orm import Session

from app.models.security.blocked_ip import (
    BlockedIP,
)

from app.repositories.base import (
    BaseRepository,
)


class BlockedIPRepository(
    BaseRepository[BlockedIP],
):
    """
    Repository responsible for blocked IP
    database operations.
    """

    def __init__( self, db: Session,) -> None:
        super().__init__(db)

    # ---------------------------------------------------------
    # Private Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _active_block_condition( current_time: datetime ):
        """
        Active blocks include:
        - Permanent blocks (blocked_until IS NULL)
        - Temporary blocks that have not expired.
        """

        return and_(
            BlockedIP.is_active.is_(True),
            or_(
                BlockedIP.blocked_until.is_(None),
                BlockedIP.blocked_until > current_time,
            ),
        )

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    def get_by_id( self, blocked_ip_id: UUID ) -> BlockedIP | None:
        statement = (
            select(BlockedIP)
            .where(
                BlockedIP.id == blocked_ip_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_public_id( self, public_id: str ) -> BlockedIP | None:

        statement = (
            select(BlockedIP)
            .where(
                BlockedIP.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_ip_address( self, ip_address: str ) -> BlockedIP | None:

        statement = (
            select(BlockedIP)
            .where(
                BlockedIP.ip_address == ip_address,
            )
        )

        return self.db.scalar(statement)

    def get_active_block( self, ip_address: str, current_time: datetime ) -> BlockedIP | None:

        statement = (
            select(BlockedIP)
            .where(
                BlockedIP.ip_address == ip_address,
            )
            .where(
                self._active_block_condition(
                    current_time,
                )
            )
        )

        return self.db.scalar(statement)

    def get_recent_blocks( self, limit: int = 100 ) -> list[BlockedIP]:

        statement = (
            select(BlockedIP)
            .order_by(
                BlockedIP.created_at.desc(),
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(statement)
        )

    def list_active_blocks( self, current_time: datetime ) -> list[BlockedIP]:

        statement = (
            select(BlockedIP)
            .where(
                self._active_block_condition(
                    current_time,
                )
            )
            .order_by(
                BlockedIP.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def list_expired_blocks( self, current_time: datetime ) -> list[BlockedIP]:

        statement = (
            select(BlockedIP)
            .where(
                BlockedIP.is_active.is_(True),
            )
            .where(
                BlockedIP.blocked_until.is_not(None),
            )
            .where(
                BlockedIP.blocked_until <= current_time,
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def exists_by_ip( self, ip_address: str ) -> bool:

        statement = (
            select(BlockedIP.id)
            .where(
                BlockedIP.ip_address == ip_address,
            )
        )

        return self.db.scalar(statement) is not None

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def count_active_blocks( self, current_time: datetime, ) -> int:

        statement = (
            select(
                func.count(
                    BlockedIP.id,
                )
            )
            .where(
                self._active_block_condition(
                    current_time,
                )
            )
        )

        return self.db.scalar(statement) or 0

    def count_expired_blocks( self, current_time: datetime ) -> int:

        statement = (
            select(
                func.count(
                    BlockedIP.id,
                )
            )
            .where(
                BlockedIP.is_active.is_(True),
            )
            .where(
                BlockedIP.blocked_until.is_not(None),
            )
            .where(
                BlockedIP.blocked_until <= current_time,
            )
        )

        return self.db.scalar(statement) or 0

    def count_permanent_blocks( self ) -> int:

        statement = (
            select(
                func.count(
                    BlockedIP.id,
                )
            )
            .where(
                BlockedIP.is_active.is_(True),
            )
            .where(
                BlockedIP.blocked_until.is_(None),
            )
        )

        return self.db.scalar(statement) or 0