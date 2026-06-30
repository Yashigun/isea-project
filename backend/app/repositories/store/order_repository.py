from __future__ import annotations

from uuid import UUID

from sqlalchemy import (
    func,
    select,
)

from sqlalchemy.orm import (
    Session,
    selectinload,
)

from app.models.store.order import (
    Order,
    OrderStatus,
)

from app.models.store.order_item import (
    OrderItem,
)

from app.repositories.base import (
    BaseRepository,
)


class OrderRepository(
    BaseRepository[Order],
):
    """
    Repository responsible for order
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
        order_id: UUID,
    ) -> Order | None:

        statement = (
            select(Order)
            .where(
                Order.id == order_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_public_id(
        self,
        public_id: str,
    ) -> Order | None:

        statement = (
            select(Order)
            .where(
                Order.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_order_details(
        self,
        public_id: str,
    ) -> Order | None:

        statement = (
            select(Order)
            .options(
                selectinload(
                    Order.items,
                ).selectinload(
                    OrderItem.product,
                ),
                selectinload(
                    Order.payment,
                ),
                selectinload(
                    Order.shipping_address,
                ),
            )
            .where(
                Order.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_customer_orders(
        self,
        customer_id: UUID,
    ) -> list[Order]:

        statement = (
            select(Order)
            .where(
                Order.customer_id == customer_id,
            )
            .order_by(
                Order.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def get_customer_order(
        self,
        customer_id: UUID,
        public_id: str,
    ) -> Order | None:

        statement = (
            select(Order)
            .options(
                selectinload(
                    Order.items,
                ).selectinload(
                    OrderItem.product,
                ),
                selectinload(
                    Order.payment,
                ),
                selectinload(
                    Order.shipping_address,
                ),
            )
            .where(
                Order.customer_id == customer_id,
            )
            .where(
                Order.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def list_by_status(
        self,
        status: OrderStatus,
    ) -> list[Order]:

        statement = (
            select(Order)
            .where(
                Order.status == status,
            )
            .order_by(
                Order.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def list_recent(
        self,
        limit: int = 20,
    ) -> list[Order]:

        statement = (
            select(Order)
            .order_by(
                Order.created_at.desc(),
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(statement)
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def count_orders(
        self,
    ) -> int:

        statement = (
            select(
                func.count(Order.id),
            )
        )

        return self.db.scalar(statement) or 0

    def count_customer_orders(
        self,
        customer_id: UUID,
    ) -> int:

        statement = (
            select(
                func.count(Order.id),
            )
            .where(
                Order.customer_id == customer_id,
            )
        )

        return self.db.scalar(statement) or 0

    def count_by_status(
        self,
        status: OrderStatus,
    ) -> int:

        statement = (
            select(
                func.count(Order.id),
            )
            .where(
                Order.status == status,
            )
        )

        return self.db.scalar(statement) or 0