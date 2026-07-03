from .auth import router as auth_router
from .products import router as products_router
from .categories import router as categories_router
from .cart import router as cart_router
from .orders import router as orders_router
from .addresses import router as addresses_router
from .phones import router as phones_router
from .wishlist import router as wishlist_router
from .reviews import router as reviews_router
from .admin import router as admin_router

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
]