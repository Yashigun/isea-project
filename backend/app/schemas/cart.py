from __future__ import annotations

from decimal import Decimal

from pydantic import (
    Field,
    field_validator,
)

from app.schemas.common import (
    BaseRequestSchema,
    BaseResponseSchema,
)

from app.schemas.product import (
    ProductSummarySchema,
)


class CartItemCreateSchema(BaseRequestSchema):
    """
    Add a product to the cart.
    """

    product_public_id: str

    quantity: int = Field(
        ge=1,
        le=99,
    )


class CartItemUpdateSchema(BaseRequestSchema):
    """
    Update the quantity of a cart item.
    """

    quantity: int = Field(
        ge=1,
        le=99,
    )


class CartItemResponseSchema(BaseResponseSchema):
    """
    Cart item returned by the API.
    """

    product: ProductSummarySchema

    quantity: int

    unit_price: Decimal

    subtotal: Decimal


class CartResponseSchema(BaseResponseSchema):
    """
    Customer shopping cart.
    """

    items: list[CartItemResponseSchema] = Field(
        default_factory=list,
    )

    total_items: int

    subtotal: Decimal

    discount: Decimal

    tax: Decimal

    total_amount: Decimal