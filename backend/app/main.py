from backend import app

from app.routes.public import (
    router as public_router,
)

app.include_router(public_router)
