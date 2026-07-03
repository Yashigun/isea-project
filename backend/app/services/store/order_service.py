from __future__ import annotations

from decimal import Decimal
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.store.order_repository import OrderRepository
from app.repositories.store.cart_repository import CartRepository
from app.repositories.store.address_repository import AddressRepository
from app.repositories.store.product_repository import ProductRepository
from app.models.store.order import Order, OrderStatus
from app.models.store.order_item import OrderItem
from app.models.store.payment import Payment, PaymentStatus, PaymentMethod


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.cart_repo = CartRepository(db)
        self.address_repo = AddressRepository(db)
        self.product_repo = ProductRepository(db)

    async def create_order(self, customer_id: UUID, address_public_id: str, notes: str | None = None) -> Order:
        # Get cart
        cart = await self.cart_repo.get_customer_cart(customer_id)
        if not cart or not cart.items:
            raise ValueError("Cart is empty")
        # Get address
        address = await self.address_repo.get_by_public_id(address_public_id)
        if not address or address.customer_id != customer_id:
            raise ValueError("Invalid address")
        # Calculate totals
        subtotal = Decimal("0")
        items = []
        for item in cart.items:
            product = await self.product_repo.get_by_id(item.product_id)
            if not product or not product.is_active:
                raise ValueError(f"Product {item.product_id} is not available")
            unit_price = product.discount_price or product.price
            item_subtotal = unit_price * item.quantity
            subtotal += item_subtotal
            items.append({
                "product_id": product.id,
                "product_name": product.name,
                "unit_price": unit_price,
                "quantity": item.quantity,
                "subtotal": item_subtotal,
            })
        # Calculate tax, shipping, discount (simplified)
        tax = subtotal * Decimal("0.10")  # 10% tax
        shipping_cost = Decimal("5.00")   # flat rate
        discount = Decimal("0")
        total = subtotal + tax + shipping_cost - discount
        # Create order
        order = Order(
            customer_id=customer_id,
            status=OrderStatus.PENDING,
            shipping_name=f"{address.customer.first_name} {address.customer.last_name}",
            shipping_phone=address.customer.phone or "",
            address_line_1=address.address_line_1,
            address_line_2=address.address_line_2,
            city=address.city,
            state=address.state,
            country=address.country,
            postal_code=address.postal_code,
            order_notes=notes,
            subtotal=subtotal,
            discount=discount,
            shipping_cost=shipping_cost,
            tax=tax,
            total_amount=total,
        )
        await self.order_repo.create(order)
        await self.db.flush()
        # Create order items
        for item_data in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data["product_id"],
                product_name=item_data["product_name"],
                unit_price=item_data["unit_price"],
                quantity=item_data["quantity"],
                subtotal=item_data["subtotal"],
            )
            self.db.add(order_item)
        # Clear cart
        for cart_item in cart.items:
            await self.db.delete(cart_item)
        await self.db.flush()
        # Create payment record (placeholder)
        payment = Payment(
            order_id=order.id,
            payment_method=PaymentMethod.CARD,  # default
            payment_status=PaymentStatus.PENDING,
            gateway_name="pending",
            transaction_reference=f"pending_{order.id.hex[:8]}",
            amount=total,
        )
        self.db.add(payment)
        await self.db.commit()
        return order

    async def get_customer_orders(self, customer_id: UUID) -> list[Order]:
        return await self.order_repo.get_customer_orders(customer_id)

    async def get_customer_order(self, customer_id: UUID, public_id: str) -> Order | None:
        return await self.order_repo.get_customer_order(customer_id, public_id)

    async def cancel_order(self, customer_id: UUID, public_id: str) -> Order:
        order = await self.order_repo.get_customer_order(customer_id, public_id)
        if not order:
            raise ValueError("Order not found")
        if order.status not in (OrderStatus.PENDING, OrderStatus.CONFIRMED):
            raise ValueError("Order cannot be cancelled")
        order.status = OrderStatus.CANCELLED
        await self.order_repo.save(order)
        await self.db.commit()
        return order