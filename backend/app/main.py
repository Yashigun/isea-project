from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import (
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
    admin_orders,
)
from app.middlewares.security_event import SecurityEventMiddleware
from app.middlewares.request_log import RequestLogMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SecurityEventMiddleware)
app.add_middleware(RequestLogMiddleware)

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
app.include_router(admin_orders, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Personal Store API is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}