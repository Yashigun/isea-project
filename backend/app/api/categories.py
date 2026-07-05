from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_admin
from app.db.database import get_db

from app.schemas.category import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
)

from app.services.store.category_service import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


# ---------------------------------------------------------------------
# PUBLIC
# ---------------------------------------------------------------------

@router.get("/", response_model=list[CategoryResponseSchema])
async def list_categories(
    active_only: bool = Query(default=True),
    db: AsyncSession = Depends(get_db),
):
    service = CategoryService(db)

    if active_only:
        return await service.list_active()

    return await service.list_all()


@router.get("/slug/{slug}", response_model=CategoryResponseSchema)
async def get_category_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    service = CategoryService(db)

    category = await service.get_by_slug(slug)

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category


@router.get("/{public_id}", response_model=CategoryResponseSchema)
async def get_category(
    public_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = CategoryService(db)

    category = await service.get_by_public_id(public_id)

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category


# ---------------------------------------------------------------------
# ADMIN
# ---------------------------------------------------------------------

@router.post(
    "/",
    response_model=CategoryResponseSchema,
    dependencies=[Depends(get_current_admin)],
)
async def create_category(
    data: CategoryCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    service = CategoryService(db)

    try:
        category = await service.create(data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    return category


@router.put(
    "/{public_id}",
    response_model=CategoryResponseSchema,
    dependencies=[Depends(get_current_admin)],
)
async def update_category(
    public_id: str,
    data: CategoryUpdateSchema,
    db: AsyncSession = Depends(get_db),
):
    service = CategoryService(db)

    try:
        category = await service.update(
            public_id,
            data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    return category


@router.delete(
    "/{public_id}",
    dependencies=[Depends(get_current_admin)],
)
async def delete_category(
    public_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = CategoryService(db)

    try:
        await service.delete(public_id)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    return {
        "message": "Category deleted",
    }