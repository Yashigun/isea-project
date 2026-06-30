from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.store.order_payment import OrderPayment
from app.models.store.payment import PaymentStatus

from app.repositories.base import BaseRepository


class PaymentRepository(
    BaseRepository[OrderPayment],
):
    """
    Repository responsible for payment
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
        payment_id: UUID,
    ) -> OrderPayment | None:

        statement = (
            select(OrderPayment)
            .where(
                OrderPayment.id == payment_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_public_id(
        self,
        public_id: str,
    ) -> OrderPayment | None:

        statement = (
            select(OrderPayment)
            .where(
                OrderPayment.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_order_id(
        self,
        order_id: UUID,
    ) -> OrderPayment | None:

        statement = (
            select(OrderPayment)
            .where(
                OrderPayment.order_id == order_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_transaction_reference(
        self,
        transaction_reference: str,
    ) -> OrderPayment | None:

        statement = (
            select(OrderPayment)
            .where(
                OrderPayment.transaction_reference
                == transaction_reference,
            )
        )

        return self.db.scalar(statement)

    def get_by_gateway_reference(
        self,
        gateway_name: str,
        transaction_reference: str,
    ) -> OrderPayment | None:

        statement = (
            select(OrderPayment)
            .where(
                OrderPayment.gateway_name == gateway_name,
            )
            .where(
                OrderPayment.transaction_reference
                == transaction_reference,
            )
        )

        return self.db.scalar(statement)

    def list_by_status(
        self,
        payment_status: PaymentStatus,
    ) -> list[OrderPayment]:

        statement = (
            select(OrderPayment)
            .where(
                OrderPayment.payment_status
                == payment_status,
            )
            .order_by(
                OrderPayment.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def payment_exists(
        self,
        transaction_reference: str,
    ) -> bool:

        statement = (
            select(OrderPayment.id)
            .where(
                OrderPayment.transaction_reference
                == transaction_reference,
            )
        )

        return self.db.scalar(statement) is not None