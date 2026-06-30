from __future__ import annotations

from uuid import UUID

from sqlalchemy import (
    func,
    select,
)

from sqlalchemy.orm import Session

from app.models.store.phone import Phone
from app.repositories.base import BaseRepository


class PhoneRepository(
    BaseRepository[Phone],
):
    """
    Repository responsible for customer
    phone number database operations.
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
        phone_id: UUID,
    ) -> Phone | None:

        statement = (
            select(Phone)
            .where(
                Phone.id == phone_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_public_id(
        self,
        public_id: str,
    ) -> Phone | None:

        statement = (
            select(Phone)
            .where(
                Phone.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_customer_phone_numbers(
        self,
        customer_id: UUID,
    ) -> list[Phone]:

        statement = (
            select(Phone)
            .where(
                Phone.customer_id == customer_id,
            )
            .order_by(
                Phone.is_default.desc(),
                Phone.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def get_default_phone(
        self,
        customer_id: UUID,
    ) -> Phone | None:

        statement = (
            select(Phone)
            .where(
                Phone.customer_id == customer_id,
            )
            .where(
                Phone.is_default.is_(True),
            )
        )

        return self.db.scalar(statement)

    def count_customer_phone_numbers(
        self,
        customer_id: UUID,
    ) -> int:

        statement = (
            select(
                func.count(Phone.id)
            )
            .where(
                Phone.customer_id == customer_id,
            )
        )

        return self.db.scalar(statement) or 0

    def belongs_to_customer(
        self,
        customer_id: UUID,
        phone_id: UUID,
    ) -> bool:

        statement = (
            select(Phone.id)
            .where(
                Phone.customer_id == customer_id,
            )
            .where(
                Phone.id == phone_id,
            )
        )

        return self.db.scalar(statement) is not None

    def get_by_phone_number(
        self,
        phone_number: str,
    ) -> Phone | None:

        statement = (
            select(Phone)
            .where(
                Phone.phone_number == phone_number,
            )
        )

        return self.db.scalar(statement)

    def exists_by_phone_number(
        self,
        phone_number: str,
    ) -> bool:

        statement = (
            select(Phone.id)
            .where(
                Phone.phone_number == phone_number,
            )
        )

        return self.db.scalar(statement) is not None