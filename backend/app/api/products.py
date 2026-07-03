from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.store.product_service import ProductService
from app.schemas.product import ProductResponseSchema, ProductCreateSchema, ProductUpdateSchema
from app.core.dependencies import get_current_admin
from typing import List

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductResponseSchema])
async def list_products(
    category: str = None,
    search: str = None,
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    if search:
        products = await service.search(search)
    elif category:
        products = await service.list_by_category(category)
    else:
        products = await service.list_active()
    return products

@router.get("/{public_id}", response_model=ProductResponseSchema)
async def get_product(public_id: str, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    product = await service.get_by_public_id(public_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/slug/{slug}", response_model=ProductResponseSchema)
async def get_product_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    product = await service.get_by_slug(slug)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Admin endpoints
@router.post("/", response_model=ProductResponseSchema  , dependencies=[Depends(get_current_admin)])
async def create_product(
    data: ProductCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    try:
        product = await service.create(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return product

@router.put("/{public_id}", response_model=ProductResponseSchema, dependencies=[Depends(get_current_admin)])
async def update_product(
    public_id: str,
    data: ProductUpdateSchema,
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    try:
        product = await service.update(public_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return product

@router.delete("/{public_id}", dependencies=[Depends(get_current_admin)])
async def delete_product(public_id: str, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    try:
        await service.delete(public_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Product deleted"}