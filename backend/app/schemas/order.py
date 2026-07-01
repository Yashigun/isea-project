from __future__ import annotations

from decimal import Decimal

from pydantic import (
    Field,
    ConfigDict,
)

from app.models.store.order import (
    OrderStatus,
)

from app.schemas.address import (
    AddressResponseSchema,
)

from app.schemas.common import (
    BaseRequestSchema,
    BaseResponseSchema,
)

from app.schemas.payment import (
    PaymentResponseSchema,
)

from app.schemas.product import (
    ProductSummarySchema,
)


# --------------------------------------------------
# Order Item
# --------------------------------------------------


class OrderItemResponseSchema(BaseResponseSchema):
    """
    Product purchased within an order.
    """

    product: ProductSummarySchema | None

    product_name: str

    unit_price: Decimal

    quantity: int

    subtotal: Decimal


# --------------------------------------------------
# Create Order
# --------------------------------------------------


class OrderCreateSchema(BaseRequestSchema):
    """
    Create an order from the current cart.
    """

    shipping_address_public_id: str

    order_notes: str | None = Field(
        default=None,
        max_length=1000,
    )


# --------------------------------------------------
# Customer Order Summary
# --------------------------------------------------


class OrderSummarySchema(BaseResponseSchema):
    """
    Lightweight order information.
    """

    status: OrderStatus

    total_amount: Decimal


# --------------------------------------------------
# Complete Order
# --------------------------------------------------


class OrderResponseSchema(OrderSummarySchema):
    """
    Complete order details.
    """

    shipping_address: AddressResponseSchema

    items: list[OrderItemResponseSchema] = Field(
        default_factory=list,
    )

    subtotal: Decimal

    discount: Decimal

    shipping_cost: Decimal

    tax: Decimal

    payment: PaymentResponseSchema | None

    order_notes: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )