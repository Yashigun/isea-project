from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.db.database import get_db
from app.services.store.product_service import ProductService
from app.services.store.cloudinary_service import CloudinaryService
from app.schemas.product import (
    ProductResponseSchema,
    ProductCreateSchema,
    ProductUpdateSchema,
)
from app.core.dependencies import get_current_admin
from app.models.store.customer import Customer
from app.models.store.product import Product

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductResponseSchema])
async def list_products(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
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
async def get_product(
    public_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    product = await service.get_by_public_id(public_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/slug/{slug}", response_model=ProductResponseSchema)
async def get_product_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    product = await service.get_by_slug(slug)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/{public_id}/related", response_model=List[ProductResponseSchema])
async def get_related_products(
    public_id: str,
    limit: int = Query(4, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    product = await service.get_by_public_id(public_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    related = await service.get_related(product.id, limit)
    return related

# -------------------- Admin Endpoints --------------------

@router.post("/", response_model=ProductResponseSchema, dependencies=[Depends(get_current_admin)])
async def create_product(
    data: ProductCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    try:
        product = await service.create(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # 🔥 Eagerly load relationships for response
    stmt = (
        select(Product)
        .where(Product.id == product.id)
        .options(
            selectinload(Product.category),
            selectinload(Product.images),
        )
    )
    result = await db.execute(stmt)
    product_with_relations = result.scalar_one()
    return product_with_relations

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
    
    # Eagerly load relationships
    stmt = (
        select(Product)
        .where(Product.public_id == public_id)
        .options(
            selectinload(Product.category),
            selectinload(Product.images),
        )
    )
    result = await db.execute(stmt)
    product_with_relations = result.scalar_one()
    return product_with_relations

@router.delete("/{public_id}", dependencies=[Depends(get_current_admin)])
async def delete_product(
    public_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    try:
        await service.delete(public_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Product deleted"}

# -------------------- Image Upload --------------------

@router.post("/upload-image", dependencies=[Depends(get_current_admin)])
async def upload_product_image(
    file: UploadFile = File(...),
    product_public_id: Optional[str] = Query(None, description="Public ID of the product to associate the image with"),
    db: AsyncSession = Depends(get_db),
    _current_admin: Customer = Depends(get_current_admin),
):
    if file.content_type not in ["image/jpeg", "image/png", "image/webp", "image/gif"]:
        raise HTTPException(status_code=400, detail="Unsupported image format.")

    file_bytes = await file.read()
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 10MB).")

    try:
        result = await CloudinaryService.upload_image(file_bytes, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Cloudinary upload failed: {str(e)}")

    if product_public_id:
        service = ProductService(db)
        image_data = {
            "url": result["url"],
            "stored_filename": result["public_id"],
            "original_filename": file.filename,
            "mime_type": file.content_type,
            "file_size": len(file_bytes),
            "sha256_hash": "",
            "alt_text": None,
            "display_order": 1,
            "is_primary": False,
        }
        try:
            image = await service.add_image(product_public_id, image_data)
            return {
                "url": result["url"],
                "public_id": result["public_id"],
                "product_image_public_id": image.public_id,
                "message": "Image uploaded and associated with product.",
            }
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Failed to associate image: {str(e)}")
    else:
        return {
            "url": result["url"],
            "public_id": result["public_id"],
            "message": "Image uploaded successfully. Provide product_public_id to associate with a product.",
        }