from __future__ import annotations

from typing import Generic, TypeVar

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

    # ---------------------------------------------------------
    # Create
    # ---------------------------------------------------------

    def create(
        self,
        instance: ModelType,
    ) -> ModelType:
        """
        Add a model instance to the current
        SQLAlchemy session.
        """

        self.db.add(instance)

        return instance

    # ---------------------------------------------------------
    # Persistence
    # ---------------------------------------------------------

    def flush(
        self,
    ) -> None:
        """
        Flush pending changes to the database
        without committing.
        """

        self.db.flush()

    def refresh(
        self,
        instance: ModelType,
    ) -> None:
        """
        Refresh an instance from the database.
        """

        self.db.refresh(instance)

    def save(
        self,
        instance: ModelType,
    ) -> ModelType:
        """
        Flush pending changes and refresh
        the instance.

        Does NOT commit the transaction.
        """

        self.flush()

        self.refresh(instance)

        return instance

    def commit(
        self,
    ) -> None:
        """
        Commit the current transaction.
        """

        self.db.commit()

    def rollback(
        self,
    ) -> None:
        """
        Roll back the current transaction.
        """

        self.db.rollback()

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def remove(
        self,
        instance: ModelType,
    ) -> None:
        """
        Mark an instance for deletion.
        """

        self.db.delete(instance)