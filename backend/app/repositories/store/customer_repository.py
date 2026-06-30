from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.store.customer import Customer
from app.repositories.base import BaseRepository


class CustomerRepository(
    BaseRepository[Customer],
):
    """
    Repository responsible only for
    customer database access.
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
        customer: Customer,
    ) -> Customer:
        """
        Add a customer to the current transaction.
        """

        return self.add(customer)

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    def get_by_id(
        self,
        customer_id: UUID,
    ) -> Customer | None:

        statement = (
            select(Customer)
            .where(
                Customer.id == customer_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_public_id(
        self,
        public_id: str,
    ) -> Customer | None:

        statement = (
            select(Customer)
            .where(
                Customer.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_email(
        self,
        email: str,
    ) -> Customer | None:

        statement = (
            select(Customer)
            .where(
                Customer.email == email,
            )
        )

        return self.db.scalar(statement)

    def exists_by_email(
        self,
        email: str,
    ) -> bool:

        statement = (
            select(Customer.id)
            .where(
                Customer.email == email,
            )
        )

        return self.db.scalar(statement) is not None

    # ---------------------------------------------------------
    # Persistence
    # ---------------------------------------------------------

    def save(
        self,
        customer: Customer,
    ) -> Customer:
        """
        Flush modified customer state
        without committing.
        """

        self.flush()

        self.refresh(customer)

        return customer

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def remove(
        self,
        customer: Customer,
    ) -> None:

        self.delete(customer)