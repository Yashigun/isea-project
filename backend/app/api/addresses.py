from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.store.address_service import AddressService
from app.schemas.address import AddressCreateSchema, AddressUpdateSchema, AddressResponseSchema
from app.core.dependencies import get_current_user
from app.models.store.customer import Customer
from typing import List

router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.get("/", response_model=List[AddressResponseSchema])
async def list_addresses(
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all addresses for the current user."""
    service = AddressService(db)
    addresses = await service.get_customer_addresses(current_user.id)
    return addresses


@router.post("/", response_model=AddressResponseSchema)
async def create_address(
    data: AddressCreateSchema,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new address."""
    service = AddressService(db)
    try:
        address = await service.create(current_user.id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return address


@router.put("/{public_id}", response_model=AddressResponseSchema)
async def update_address(
    public_id: str,
    data: AddressUpdateSchema,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update an existing address."""
    service = AddressService(db)
    try:
        address = await service.update(current_user.id, public_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return address


@router.delete("/{public_id}")
async def delete_address(
    public_id: str,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete an address."""
    service = AddressService(db)
    try:
        await service.delete(current_user.id, public_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Address deleted"}


@router.post("/{public_id}/set-default")
async def set_default_address(
    public_id: str,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Set an address as the default."""
    service = AddressService(db)
    try:
        await service.set_default(current_user.id, public_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Default address updated"}