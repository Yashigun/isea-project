from __future__ import annotations

from uuid import UUID

from sqlalchemy import (
    select,
)

from sqlalchemy.orm import (
    Session,
    selectinload,
)

from app.models.store.wishlist_item import (
    WishlistItem,
)

from app.repositories.base import (
    BaseRepository,
)


class WishlistRepository(
    BaseRepository[WishlistItem],
):
    """
    Repository responsible for customer
    wishlist database operations.
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
        wishlist_item_id: UUID,
    ) -> WishlistItem | None:

        statement = (
            select(WishlistItem)
            .where(
                WishlistItem.id == wishlist_item_id,
            )
        )

        return self.db.scalar(statement)

    def get_customer_wishlist(
        self,
        customer_id: UUID,
    ) -> list[WishlistItem]:

        statement = (
            select(WishlistItem)
            .options(
                selectinload(
                    WishlistItem.product,
                )
            )
            .where(
                WishlistItem.customer_id == customer_id,
            )
            .order_by(
                WishlistItem.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def get_item(
        self,
        customer_id: UUID,
        product_id: UUID,
    ) -> WishlistItem | None:

        statement = (
            select(WishlistItem)
            .where(
                WishlistItem.customer_id == customer_id,
            )
            .where(
                WishlistItem.product_id == product_id,
            )
        )

        return self.db.scalar(statement)

    def exists(
        self,
        customer_id: UUID,
        product_id: UUID,
    ) -> bool:

        statement = (
            select(WishlistItem.id)
            .where(
                WishlistItem.customer_id == customer_id,
            )
            .where(
                WishlistItem.product_id == product_id,
            )
        )

        return self.db.scalar(statement) is not None

    def count_customer_items(
        self,
        customer_id: UUID,
    ) -> int:

        statement = (
            select(WishlistItem.id)
            .where(
                WishlistItem.customer_id == customer_id,
            )
        )

        return len(
            list(
                self.db.scalars(statement)
            )
        )