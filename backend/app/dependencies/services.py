from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.services.storefront.category_service import (
    CategoryService,
)
from app.services.storefront.product_service import (
    ProductService,
)


def get_category_service(
    db: Session = Depends(get_db),
) -> CategoryService:
    """
    Dependency that provides a CategoryService.
    """

    return CategoryService(db)


def get_product_service(
    db: Session = Depends(get_db),
) -> ProductService:
    """
    Dependency that provides a ProductService.
    """

    return ProductService(db)