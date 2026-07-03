from app.routes import (
    auth_router,
    products_router,
    categories_router,
    cart_router,
    orders_router,
    addresses_router,
    phones_router,
    wishlist_router,
    reviews_router,
    admin_router,
)
from backend import app

from app.middlewares.request_log import RequestLogMiddleware
from app.middlewares.security_events import SecurityEventMiddleware

app.add_middleware(RequestLogMiddleware)
app.add_middleware(SecurityEventMiddleware)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(products_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")
app.include_router(cart_router, prefix="/api/v1")
app.include_router(orders_router, prefix="/api/v1")
app.include_router(addresses_router, prefix="/api/v1")
app.include_router(phones_router, prefix="/api/v1")
app.include_router(wishlist_router, prefix="/api/v1")
app.include_router(reviews_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")