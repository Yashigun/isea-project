from __future__ import annotations

from datetime import datetime, timezone
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


T = TypeVar("T")


class ErrorDetail(BaseModel):
    """
    Standard error payload.
    """

    code: str
    message: str


class SuccessResponse(GenericModel, Generic[T]):
    """
    Standard successful API response.
    """

    success: bool = True

    message: str

    data: T

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    request_id: UUID | None = None


class ErrorResponse(BaseModel):
    """
    Standard failed API response.
    """

    success: bool = False

    error: ErrorDetail

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    request_id: UUID | None = None