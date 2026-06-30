from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import (
    ConfigDict,
)

from app.models.store.payment import (
    PaymentMethod,
    PaymentStatus,
)

from app.schemas.common import (
    BaseResponseSchema,
)


class PaymentResponseSchema(BaseResponseSchema):
    """
    Payment information returned to customers.
    """

    payment_method: PaymentMethod

    payment_status: PaymentStatus

    amount: Decimal

    paid_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class PaymentAdminResponseSchema(PaymentResponseSchema):
    """
    Extended payment information for administrators.
    """

    gateway_name: str

    transaction_reference: str