from __future__ import annotations

from typing import (
    Generic,
    TypeVar,
)

from sqlalchemy.orm import Session


ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Base repository providing common database
    operations for all repositories.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db

    def add(
        self,
        instance: ModelType,
    ) -> ModelType:
        """
        Add a model instance to the session.
        """

        self.db.add(instance)

        return instance

    def flush(self) -> None:
        """
        Flush pending changes to the database
        without committing.
        """

        self.db.flush()

    def commit(self) -> None:
        """
        Commit the current transaction.
        """

        self.db.commit()

    def rollback(self) -> None:
        """
        Roll back the current transaction.
        """

        self.db.rollback()

    def refresh(
        self,
        instance: ModelType,
    ) -> None:
        """
        Refresh an instance from the database.
        """

        self.db.refresh(instance)

    def delete(
        self,
        instance: ModelType,
    ) -> None:
        """
        Delete a model instance.
        """

        self.db.delete(instance)
        
    def create(
        self,
        instance: ModelType,
    ) -> ModelType:

        self.db.add(instance)

        return instance

    def save(
        self,
        instance: ModelType,
    ) -> ModelType:

        self.flush()

        self.refresh(instance)

        return instance

    def remove(
        self,
        instance: ModelType,
    ) -> None:

        self.db.delete(instance)