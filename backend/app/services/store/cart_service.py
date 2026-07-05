from __future__ import annotations

from decimal import Decimal
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.store.cart_repository import CartRepository
from app.repositories.store.product_repository import ProductRepository
from app.models.store.cart import Cart
from app.models.store.cart_item import CartItem


class CartService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.cart_repo = CartRepository(db)
        self.product_repo = ProductRepository(db)

    async def get_cart(self, customer_id: UUID) -> Cart | None:
        cart = await self.cart_repo.get_customer_cart(customer_id)
        if cart:
            return cart
        cart = Cart(customer_id=customer_id)
        await self.cart_repo.create(cart)
        await self.db.commit()
        return await self.cart_repo.get_customer_cart(customer_id) or cart

    async def add_item(self, customer_id: UUID, product_public_id: str, quantity: int) -> Cart:
        product = await self.product_repo.get_active_by_public_id(product_public_id)
        if not product:
            raise ValueError("Product not found")
        # Get or create cart
        cart = await self.cart_repo.get_customer_cart(customer_id)
        if not cart:
            cart = Cart(customer_id=customer_id)
            await self.cart_repo.create(cart)
            await self.db.flush()
        # Check if item exists
        existing = await self.cart_repo.get_cart_item(cart.id, product.id)
        if existing:
            existing.quantity += quantity
            await self.cart_repo.save(existing)
        else:
            item = CartItem(
                cart_id=cart.id,
                product_id=product.id,
                quantity=quantity,
            )
            self.db.add(item)
            await self.db.flush()
        await self.db.commit()
        refreshed = await self.cart_repo.get_customer_cart(customer_id)
        return refreshed or cart

    async def update_quantity(self, customer_id: UUID, product_public_id: str, quantity: int) -> Cart:
        product = await self.product_repo.get_active_by_public_id(product_public_id)
        if not product:
            raise ValueError("Product not found")
        cart = await self.cart_repo.get_customer_cart(customer_id)
        if not cart:
            raise ValueError("Cart not found")
        item = await self.cart_repo.get_cart_item(cart.id, product.id)
        if not item:
            raise ValueError("Item not in cart")
        if quantity <= 0:
            await self.db.delete(item)
            await self.db.flush()
        else:
            item.quantity = quantity
            await self.cart_repo.save(item)
        await self.db.commit()
        refreshed = await self.cart_repo.get_customer_cart(customer_id)
        return refreshed or cart

    async def remove_item(self, customer_id: UUID, product_public_id: str) -> Cart:
        return await self.update_quantity(customer_id, product_public_id, 0)

    async def clear_cart(self, customer_id: UUID) -> None:
        cart = await self.cart_repo.get_customer_cart(customer_id)
        if cart:
            for item in cart.items:
                await self.db.delete(item)
            await self.db.flush()
            await self.db.commit()
