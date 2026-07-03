from __future__ import annotations

from typing import Generic, TypeVar, Type, Optional, List, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base repository providing common async database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.model: Type[ModelType] = self._get_model()

    def _get_model(self) -> Type[ModelType]:
        raise NotImplementedError("Subclasses must specify their model.")

    # ---------------------------------------------------------
    # Create
    # ---------------------------------------------------------

    async def create(self, instance: ModelType) -> ModelType:
        self.db.add(instance)
        await self.db.flush()
        return instance

    # ---------------------------------------------------------
    # Persistence
    # ---------------------------------------------------------

    async def flush(self) -> None:
        await self.db.flush()

    async def refresh(self, instance: ModelType) -> None:
        await self.db.refresh(instance)

    async def save(self, instance: ModelType) -> ModelType:
        await self.flush()
        await self.refresh(instance)
        return instance

    async def commit(self) -> None:
        await self.db.commit()

    async def rollback(self) -> None:
        await self.db.rollback()

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    async def remove(self, instance: ModelType) -> None:
        await self.db.delete(instance)
        await self.flush()

    # ---------------------------------------------------------
    # Read
    # ---------------------------------------------------------

    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_public_id(self, public_id: str) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.public_id == public_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self, **filters) -> List[ModelType]:
        stmt = select(self.model).filter_by(**filters)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())