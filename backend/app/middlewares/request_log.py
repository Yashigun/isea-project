from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time
import uuid
from app.services.security.request_log_service import log_request_async


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start = time.time()
        response = await call_next(request)
        duration_ms = (time.time() - start) * 1000

        # Fire-and-forget logging
        import asyncio
        asyncio.create_task(log_request_async(request, response, duration_ms))

        return response