from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseRequestSchema(BaseModel):
    """
    Base class for all request schemas.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


class BaseResponseSchema(BaseModel):
    """
    Base class for all response schemas.
    """

    public_id: str

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )