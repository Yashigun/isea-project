from __future__ import annotations

from uuid import UUID

from sqlalchemy import (
    func,
    select,
)

from sqlalchemy.orm import Session

from app.models.store.address import Address
from app.repositories.base import BaseRepository


class AddressRepository(
    BaseRepository[Address],
):
    """
    Repository responsible for customer
    address database operations.
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
        address_id: UUID,
    ) -> Address | None:

        statement = (
            select(Address)
            .where(
                Address.id == address_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_public_id(
        self,
        public_id: str,
    ) -> Address | None:

        statement = (
            select(Address)
            .where(
                Address.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_customer_addresses(
        self,
        customer_id: UUID,
    ) -> list[Address]:

        statement = (
            select(Address)
            .where(
                Address.customer_id == customer_id,
            )
            .order_by(
                Address.is_default.desc(),
                Address.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def get_default_address(
        self,
        customer_id: UUID,
    ) -> Address | None:

        statement = (
            select(Address)
            .where(
                Address.customer_id == customer_id,
            )
            .where(
                Address.is_default.is_(True),
            )
        )

        return self.db.scalar(statement)

    def count_customer_addresses(
        self,
        customer_id: UUID,
    ) -> int:

        statement = (
            select(
                func.count(Address.id)
            )
            .where(
                Address.customer_id == customer_id,
            )
        )

        return self.db.scalar(statement) or 0

    def exists(
        self,
        customer_id: UUID,
        address_id: UUID,
    ) -> bool:

        statement = (
            select(Address.id)
            .where(
                Address.customer_id == customer_id,
            )
            .where(
                Address.id == address_id,
            )
        )

        return self.db.scalar(statement) is not None