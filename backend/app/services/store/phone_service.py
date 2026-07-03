from __future__ import annotations

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.store.phone_repository import PhoneRepository
from app.models.store.phone_number import PhoneNumber
from app.schemas.customer import CustomerPhoneSchema


class PhoneService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = PhoneRepository(db)

    async def get_customer_phones(self, customer_id: UUID) -> List[PhoneNumber]:
        return await self.repo.get_customer_phone_numbers(customer_id)

    async def get_by_id(self, customer_id: UUID, phone_id: UUID) -> Optional[PhoneNumber]:
        phone = await self.repo.get_by_id(phone_id)
        if phone and phone.customer_id == customer_id:
            return phone
        return None

    async def get_by_public_id(self, customer_id: UUID, public_id: str) -> Optional[PhoneNumber]:
        phone = await self.repo.get_by_public_id(public_id)
        if phone and phone.customer_id == customer_id:
            return phone
        return None

    async def create(self, customer_id: UUID, data: CustomerPhoneSchema) -> PhoneNumber:
        # Check if phone number already exists for this customer
        existing = await self.repo.get_by_phone_number(data.phone_number)
        if existing and existing.customer_id == customer_id:
            raise ValueError("Phone number already exists")
        count = await self.repo.count_customer_phone_numbers(customer_id)
        is_default = data.is_default if count > 0 else True
        if is_default:
            current_default = await self.repo.get_default_phone(customer_id)
            if current_default:
                current_default.is_default = False
                await self.repo.save(current_default)
        phone = PhoneNumber(
            customer_id=customer_id,
            phone_number=data.phone_number,
            is_default=is_default,
        )
        await self.repo.create(phone)
        await self.db.commit()
        return phone

    async def update(self, customer_id: UUID, public_id: str, data: CustomerPhoneSchema) -> PhoneNumber:
        phone = await self.repo.get_by_public_id(public_id)
        if not phone or phone.customer_id != customer_id:
            raise ValueError("Phone number not found")
        if data.phone_number != phone.phone_number:
            # Check uniqueness
            existing = await self.repo.get_by_phone_number(data.phone_number)
            if existing and existing.id != phone.id:
                raise ValueError("Phone number already exists")
            phone.phone_number = data.phone_number
        if data.is_default != phone.is_default:
            if data.is_default:
                current_default = await self.repo.get_default_phone(customer_id)
                if current_default and current_default.id != phone.id:
                    current_default.is_default = False
                    await self.repo.save(current_default)
            phone.is_default = data.is_default
        await self.repo.save(phone)
        await self.db.commit()
        return phone

    async def delete(self, customer_id: UUID, public_id: str) -> None:
        phone = await self.repo.get_by_public_id(public_id)
        if not phone or phone.customer_id != customer_id:
            raise ValueError("Phone number not found")
        if phone.is_default:
            others = await self.repo.get_customer_phone_numbers(customer_id)
            others = [p for p in others if p.id != phone.id]
            if others:
                others[0].is_default = True
                await self.repo.save(others[0])
        await self.repo.remove(phone)
        await self.db.commit()

    async def set_default(self, customer_id: UUID, public_id: str) -> None:
        phone = await self.repo.get_by_public_id(public_id)
        if not phone or phone.customer_id != customer_id:
            raise ValueError("Phone number not found")
        current_default = await self.repo.get_default_phone(customer_id)
        if current_default and current_default.id != phone.id:
            current_default.is_default = False
            await self.repo.save(current_default)
        phone.is_default = True
        await self.repo.save(phone)
        await self.db.commit()