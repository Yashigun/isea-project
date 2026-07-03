from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.store.phone_service import PhoneService
from app.schemas.customer import CustomerPhoneSchema, CustomerPhoneResponseSchema
from app.core.dependencies import get_current_user
from app.models.store.customer import Customer
from typing import List

router = APIRouter(prefix="/phones", tags=["phones"])


@router.get("/", response_model=List[CustomerPhoneResponseSchema])
async def list_phones(
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all phone numbers for the current user."""
    service = PhoneService(db)
    phones = await service.get_customer_phones(current_user.id)
    return phones


@router.post("/", response_model=CustomerPhoneResponseSchema)
async def create_phone(
    data: CustomerPhoneSchema,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add a new phone number."""
    service = PhoneService(db)
    try:
        phone = await service.create(current_user.id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return phone


@router.put("/{public_id}", response_model=CustomerPhoneResponseSchema)
async def update_phone(
    public_id: str,
    data: CustomerPhoneSchema,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update an existing phone number."""
    service = PhoneService(db)
    try:
        phone = await service.update(current_user.id, public_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return phone


@router.delete("/{public_id}")
async def delete_phone(
    public_id: str,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a phone number."""
    service = PhoneService(db)
    try:
        await service.delete(current_user.id, public_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Phone number deleted"}


@router.post("/{public_id}/set-default")
async def set_default_phone(
    public_id: str,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Set a phone number as default."""
    service = PhoneService(db)
    try:
        await service.set_default(current_user.id, public_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Default phone updated"}