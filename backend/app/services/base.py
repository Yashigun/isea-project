from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session


SchemaType = TypeVar(
    "SchemaType",
    bound=BaseModel,
)


class BaseService:
    """
    Base class for all business services.

    Provides:
    - Database session
    - Logging
    - Schema mapping helpers
    """

    logger = logging.getLogger(__name__)

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db

    # ---------------------------------------------------------
    # Schema Helpers
    # ---------------------------------------------------------

    @staticmethod
    def to_schema(
        obj,
        schema: type[SchemaType],
    ) -> SchemaType:

        return schema.model_validate(obj)

    @staticmethod
    def to_schema_list(
        objects: Sequence,
        schema: type[SchemaType],
    ) -> list[SchemaType]:

        return [
            schema.model_validate(item)
            for item in objects
        ]