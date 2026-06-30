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

from app.models.store.cart import Cart
from app.models.store.cart_item import CartItem
from app.models.store.product import Product

from app.repositories.base import BaseRepository


class CartRepository(
    BaseRepository[Cart],
):
    """
    Repository responsible for shopping cart
    database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

    # ---------------------------------------------------------
    # Cart
    # ---------------------------------------------------------

    def get_by_id(
        self,
        cart_id: UUID,
    ) -> Cart | None:

        statement = (
            select(Cart)
            .where(
                Cart.id == cart_id,
            )
        )

        return self.db.scalar(statement)

    def get_by_public_id(
        self,
        public_id: str,
    ) -> Cart | None:

        statement = (
            select(Cart)
            .where(
                Cart.public_id == public_id,
            )
        )

        return self.db.scalar(statement)

    def get_customer_cart(
        self,
        customer_id: UUID,
    ) -> Cart | None:

        statement = (
            select(Cart)
            .options(
                selectinload(
                    Cart.items
                )
                .selectinload(
                    CartItem.product
                )
                .selectinload(
                    Product.images
                )
            )
            .where(
                Cart.customer_id == customer_id,
            )
        )

        return self.db.scalar(statement)

    # ---------------------------------------------------------
    # Cart Items
    # ---------------------------------------------------------

    def get_cart_item(
        self,
        cart_id: UUID,
        product_id: UUID,
    ) -> CartItem | None:

        statement = (
            select(CartItem)
            .where(
                CartItem.cart_id == cart_id,
            )
            .where(
                CartItem.product_id == product_id,
            )
        )

        return self.db.scalar(statement)

    def get_cart_items(
        self,
        cart_id: UUID,
    ) -> list[CartItem]:

        statement = (
            select(CartItem)
            .options(
                selectinload(
                    CartItem.product
                )
                .selectinload(
                    Product.images
                )
            )
            .where(
                CartItem.cart_id == cart_id,
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def count_cart_items(
        self,
        cart_id: UUID,
    ) -> int:

        statement = (
            select(
                func.count(CartItem.id)
            )
            .where(
                CartItem.cart_id == cart_id,
            )
        )

        return self.db.scalar(statement) or 0

    def get_total_quantity(
        self,
        cart_id: UUID,
    ) -> int:

        statement = (
            select(
                func.coalesce(
                    func.sum(
                        CartItem.quantity
                    ),
                    0,
                )
            )
            .where(
                CartItem.cart_id == cart_id,
            )
        )

        return self.db.scalar(statement) or 0

    def item_exists(
        self,
        cart_id: UUID,
        product_id: UUID,
    ) -> bool:

        statement = (
            select(CartItem.id)
            .where(
                CartItem.cart_id == cart_id,
            )
            .where(
                CartItem.product_id == product_id,
            )
        )

        return self.db.scalar(statement) is not None