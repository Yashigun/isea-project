from __future__ import annotations

from datetime import datetime
from typing import Optional

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

    created_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
    )