from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import re
import asyncio
from app.services.security_service import create_security_event  # we'll define this helper below


# Patterns for detection
SQL_INJECTION_PATTERNS = [
    re.compile(r"(?i)(\bselect\b.*\bfrom\b|\bunion\b.*\bselect\b|\binsert\b.*\binto\b|\bdelete\b.*\bfrom\b|\bdrop\b.*\btable\b|\bupdate\b.*\bset\b)"),
]
XSS_PATTERNS = [
    re.compile(r"(?i)(<script.*?>.*?</script>|on\w+\s*=|javascript:)"),
]
PATH_TRAVERSAL_PATTERNS = [
    re.compile(r"(\.\./|\.\.\\)"),
]
SUSPICIOUS_PARAMS = ["'", '"', "=", "union", "select", "drop", "insert", "update", "delete", "exec", "xp_", "cmd", "powershell"]


class SecurityEventMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check request for suspicious patterns
        ip = request.client.host if request.client else "0.0.0.0"
        path = request.url.path
        query = str(request.query_params)

        # Check for SQL injection
        if any(p.search(query) for p in SQL_INJECTION_PATTERNS):
            await self._create_event(
                event_type="sql_injection",
                severity="high",
                title="SQL Injection Attempt",
                description=f"SQL injection pattern detected in query: {query}",
                ip=ip,
                request=request,
            )

        # Check for XSS
        if any(p.search(query) for p in XSS_PATTERNS):
            await self._create_event(
                event_type="xss",
                severity="high",
                title="XSS Attempt",
                description=f"XSS pattern detected in query: {query}",
                ip=ip,
                request=request,
            )

        # Check for path traversal
        if any(p.search(path) for p in PATH_TRAVERSAL_PATTERNS):
            await self._create_event(
                event_type="path_traversal",
                severity="medium",
                title="Path Traversal Attempt",
                description=f"Path traversal pattern detected in path: {path}",
                ip=ip,
                request=request,
            )

        # Proceed with request
        response = await call_next(request)
        return response

    async def _create_event(self, event_type, severity, title, description, ip, request):
        # Use background task to avoid blocking
        from app.services.security_service import create_security_event_async
        asyncio.create_task(create_security_event_async(
            event_type=event_type,
            severity=severity,
            title=title,
            description=description,
            ip=ip,
            request_id=getattr(request.state, "request_id", None),
            evidence={"query": str(request.query_params), "path": request.url.path},
        ))