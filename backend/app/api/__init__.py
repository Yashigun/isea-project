from app.api.auth import router as auth_router
from app.api.products import router as products_router
from app.api.categories import router as categories_router
from app.api.cart import router as cart_router
from app.api.orders import router as orders_router
from app.api.addresses import router as addresses_router
from app.api.phones import router as phones_router
from app.api.wishlist import router as wishlist_router
from app.api.reviews import router as reviews_router
from app.api.admin import router as admin_router
from app.api.admin_orders import router as admin_orders  

__all__ = [
    "auth_router",
    "products_router",
    "categories_router",
    "cart_router",
    "orders_router",
    "addresses_router",
    "phones_router",
    "wishlist_router",
    "reviews_router",
    "admin_router",
    "admin_orders",
]