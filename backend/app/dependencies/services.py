from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db

# Services
from app.services.security.auth_service import AuthService
from app.services.store.product_service import ProductService
from app.services.store.category_service import CategoryService
from app.services.store.cart_service import CartService
from app.services.store.order_service import OrderService
from app.services.store.address_service import AddressService
from app.services.store.phone_service import PhoneService
from app.services.store.wishlist_service import WishlistService
from app.services.store.review_service import ReviewService
from app.services.security.security_service import SecurityService

# Async dependencies
async def get_auth_service(
    db: AsyncSession = Depends(get_db),
) -> AuthService:
    return AuthService(db)

async def get_product_service(
    db: AsyncSession = Depends(get_db),
) -> ProductService:
    return ProductService(db)

async def get_category_service(
    db: AsyncSession = Depends(get_db),
) -> CategoryService:
    return CategoryService(db)

async def get_cart_service(
    db: AsyncSession = Depends(get_db),
) -> CartService:
    return CartService(db)

async def get_order_service(
    db: AsyncSession = Depends(get_db),
) -> OrderService:
    return OrderService(db)

async def get_address_service(
    db: AsyncSession = Depends(get_db),
) -> AddressService:
    return AddressService(db)

async def get_phone_service(
    db: AsyncSession = Depends(get_db),
) -> PhoneService:
    return PhoneService(db)

async def get_wishlist_service(
    db: AsyncSession = Depends(get_db),
) -> WishlistService:
    return WishlistService(db)

async def get_review_service(
    db: AsyncSession = Depends(get_db),
) -> ReviewService:
    return ReviewService(db)

async def get_security_service(
    db: AsyncSession = Depends(get_db),
) -> SecurityService:
    return SecurityService(db)