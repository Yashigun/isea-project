from __future__ import annotations

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.store.address_repository import AddressRepository
from app.models.store.address import Address
from app.schemas.address import AddressCreateSchema, AddressUpdateSchema


class AddressService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AddressRepository(db)

    async def get_customer_addresses(self, customer_id: UUID) -> List[Address]:
        return await self.repo.get_customer_addresses(customer_id)

    async def get_by_id(self, customer_id: UUID, address_id: UUID) -> Optional[Address]:
        address = await self.repo.get_by_id(address_id)
        if address and address.customer_id == customer_id:
            return address
        return None

    async def get_by_public_id(self, customer_id: UUID, public_id: str) -> Optional[Address]:
        address = await self.repo.get_by_public_id(public_id)
        if address and address.customer_id == customer_id:
            return address
        return None

    async def create(self, customer_id: UUID, data: AddressCreateSchema) -> Address:
        # If this is the first address, make it default
        count = await self.repo.count_customer_addresses(customer_id)
        is_default = data.is_default if count > 0 else True
        if is_default:
            # Clear any existing default
            current_default = await self.repo.get_default_address(customer_id)
            if current_default:
                current_default.is_default = False
                await self.repo.save(current_default)
        address = Address(
            customer_id=customer_id,
            address_line_1=data.address_line_1,
            address_line_2=data.address_line_2,
            city=data.city,
            state=data.state,
            country=data.country,
            postal_code=data.postal_code,
            is_default=is_default,
        )
        await self.repo.create(address)
        await self.db.commit()
        return address

    async def update(self, customer_id: UUID, public_id: str, data: AddressUpdateSchema) -> Address:
        address = await self.repo.get_by_public_id(public_id)
        if not address or address.customer_id != customer_id:
            raise ValueError("Address not found")
        if data.address_line_1 is not None:
            address.address_line_1 = data.address_line_1
        if data.address_line_2 is not None:
            address.address_line_2 = data.address_line_2
        if data.city is not None:
            address.city = data.city
        if data.state is not None:
            address.state = data.state
        if data.country is not None:
            address.country = data.country
        if data.postal_code is not None:
            address.postal_code = data.postal_code
        if data.is_default is not None and data.is_default != address.is_default:
            # If setting to default, clear others
            if data.is_default:
                current_default = await self.repo.get_default_address(customer_id)
                if current_default and current_default.id != address.id:
                    current_default.is_default = False
                    await self.repo.save(current_default)
            address.is_default = data.is_default
        await self.repo.save(address)
        await self.db.commit()
        return address

    async def delete(self, customer_id: UUID, public_id: str) -> None:
        address = await self.repo.get_by_public_id(public_id)
        if not address or address.customer_id != customer_id:
            raise ValueError("Address not found")
        # If this is the default address, maybe set another as default?
        if address.is_default:
            # Try to set another address as default
            others = await self.repo.get_customer_addresses(customer_id)
            others = [a for a in others if a.id != address.id]
            if others:
                others[0].is_default = True
                await self.repo.save(others[0])
        await self.repo.remove(address)
        await self.db.commit()

    async def set_default(self, customer_id: UUID, public_id: str) -> None:
        address = await self.repo.get_by_public_id(public_id)
        if not address or address.customer_id != customer_id:
            raise ValueError("Address not found")
        # Clear existing default
        current_default = await self.repo.get_default_address(customer_id)
        if current_default and current_default.id != address.id:
            current_default.is_default = False
            await self.repo.save(current_default)
        address.is_default = True
        await self.repo.save(address)
        await self.db.commit()