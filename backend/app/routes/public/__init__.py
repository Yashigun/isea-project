from fastapi import APIRouter

from app.routes.public.categories import (
    router as category_router,
)

from app.routes.public.products import (
    router as product_router,
)

router = APIRouter()

router.include_router(category_router)

router.include_router(product_router)