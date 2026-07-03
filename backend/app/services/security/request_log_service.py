from __future__ import annotations

from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal
from app.models.security.request_log import (
    RequestLog,
    HttpMethod,
    HttpProtocol,
    RequestSource,
    RequestOutcome,
)


async def log_request_async(request: Request, response: Response, duration_ms: int) -> None:
    """
    Fire-and-forget async logging of every request.
    """
    try:
        async with AsyncSessionLocal() as db:
            # Get customer_id from request.state if set by auth middleware
            customer_id = getattr(request.state, "customer_id", None)
            session_id = getattr(request.state, "session_id", None)

            # Determine protocol (simplified)
            protocol = HttpProtocol.HTTP_1_1
            if "HTTP/2" in request.headers.get("http_version", ""):
                protocol = HttpProtocol.HTTP_2

            # Determine source (simple heuristic)
            user_agent = request.headers.get("user-agent", "")
            source = RequestSource.API
            if "Mobile" in user_agent or "Android" in user_agent or "iPhone" in user_agent:
                source = RequestSource.MOBILE
            elif "Mozilla" in user_agent:
                source = RequestSource.WEB

            log = RequestLog(
                request_id=request.state.request_id,
                customer_id=customer_id,
                session_id=session_id,
                method=HttpMethod(request.method),
                protocol=protocol,
                source=source,
                outcome=_get_outcome(response.status_code),
                route=request.url.path,
                path=request.url.path,
                query_string=str(request.query_params) if request.query_params else None,
                status_code=response.status_code,
                request_size=0,  # Can be computed but omitted for performance
                response_size=0,
                response_time_ms=duration_ms,
                ip_address=request.client.host if request.client else "0.0.0.0",
                user_agent=user_agent,
                referer=request.headers.get("referer"),
            )
            db.add(log)
            await db.commit()
    except Exception:
        # Logging should never break the request
        pass


def _get_outcome(status: int) -> RequestOutcome:
    if 200 <= status < 300:
        return RequestOutcome.SUCCESS
    if 300 <= status < 400:
        return RequestOutcome.REDIRECT
    if 400 <= status < 500:
        return RequestOutcome.CLIENT_ERROR
    return RequestOutcome.SERVER_ERROR