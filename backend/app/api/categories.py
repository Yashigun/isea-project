from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.store.category_service import CategoryService
from app.schemas.category import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
)
from app.core.dependencies import get_current_admin, get_current_user
from typing import List

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryResponseSchema])
async def list_categories(
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
):
    """List all categories, optionally only active ones."""
    service = CategoryService(db)
    if active_only:
        categories = await service.list_active()
    else:
        categories = await service.list_all()
    return categories


@router.get("/{public_id}", response_model=CategoryResponseSchema)
async def get_category(
    public_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a single category by public ID."""
    service = CategoryService(db)
    category = await service.get_by_public_id(public_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/slug/{slug}", response_model=CategoryResponseSchema)
async def get_category_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a category by its slug."""
    service = CategoryService(db)
    category = await service.get_by_slug(slug)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# Admin endpoints
@router.post("/", response_model=CategoryResponseSchema, dependencies=[Depends(get_current_admin)])
async def create_category(
    data: CategoryCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    """Create a new category (admin only)."""
    service = CategoryService(db)
    try:
        category = await service.create(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return category


@router.put("/{public_id}", response_model=CategoryResponseSchema, dependencies=[Depends(get_current_admin)])
async def update_category(
    public_id: str,
    data: CategoryUpdateSchema,
    db: AsyncSession = Depends(get_db),
):
    """Update an existing category (admin only)."""
    service = CategoryService(db)
    try:
        category = await service.update(public_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return category


@router.delete("/{public_id}", dependencies=[Depends(get_current_admin)])
async def delete_category(
    public_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Delete a category (admin only)."""
    service = CategoryService(db)
    try:
        await service.delete(public_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Category deleted"}