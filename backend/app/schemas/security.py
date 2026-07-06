from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.schemas.common import BaseResponseSchema

from app.models.security.audit_log import (
    AuditAction,
    EntityType,
)

from app.models.security.blocked_ip import (
    BlockReason,
)

from app.models.security.login_attempt import (
    AttemptType,
    AuthenticationFailureReason,
)

from app.models.security.request_log import (
    HttpMethod,
    HttpProtocol,
    RequestSource,
    RequestOutcome,
)

from app.models.security.security_event import (
    EventSeverity,
    SecurityEventType,
)


# -------------------------------------------------------
# Security Events
# -------------------------------------------------------

class SecurityEventResponse(BaseResponseSchema):
    event_type: SecurityEventType
    severity: EventSeverity
    title: str
    description: str
    ip_address: IPv4Address | IPv6Address
    country: Optional[str] = None
    city: Optional[str] = None
    resolved: bool
    evidence: Optional[dict] = None


# -------------------------------------------------------
# Request Logs
# -------------------------------------------------------

class RequestLogResponse(BaseResponseSchema):
    method: HttpMethod
    protocol: HttpProtocol
    source: RequestSource
    outcome: RequestOutcome
    route: str
    path: str
    query_string: str | None = None
    status_code: int
    response_time_ms: int
    ip_address: IPv4Address | IPv6Address
    user_agent: str
    country: str | None = None
    city: str | None = None
    customer_id: UUID | None = None


class RequestLogListResponse(BaseModel):
    items: list[RequestLogResponse]
    total: int
    limit: int
    offset: int


# -------------------------------------------------------
# Customer Sessions
# -------------------------------------------------------

class CustomerSessionResponse(BaseResponseSchema):
    customer_id: UUID

    device_name: str | None = None
    browser: str | None = None
    operating_system: str | None = None

    ip_address: IPv4Address | IPv6Address
    user_agent: str

    country: str | None = None
    city: str | None = None

    login_at: datetime
    last_activity: datetime
    expires_at: datetime
    revoked_at: datetime | None = None


class CustomerSessionListResponse(BaseModel):
    items: list[CustomerSessionResponse]
    total: int
    limit: int
    offset: int


# -------------------------------------------------------
# Login Attempts
# -------------------------------------------------------

class LoginAttemptResponse(BaseResponseSchema):
    email: str
    ip_address: IPv4Address | IPv6Address
    user_agent: str
    successful: bool
    failure_reason: AuthenticationFailureReason | None = None
    attempt_type: AttemptType
    customer_id: UUID | None = None


class LoginAttemptListResponse(BaseModel):
    items: list[LoginAttemptResponse]
    total: int
    limit: int
    offset: int


# -------------------------------------------------------
# Audit Logs
# -------------------------------------------------------

class AuditLogResponse(BaseResponseSchema):
    action: AuditAction
    entity_type: EntityType
    entity_name: str | None = None
    entity_public_id: str | None = None
    old_data: dict | None = None
    new_data: dict | None = None
    ip_address: IPv4Address | IPv6Address
    user_agent: str
    customer_id: UUID | None = None


class AuditLogListResponse(BaseModel):
    items: list[AuditLogResponse]
    total: int
    limit: int
    offset: int


# -------------------------------------------------------
# Blocked IPs
# -------------------------------------------------------

class BlockedIPResponse(BaseResponseSchema):
    ip_address: IPv4Address | IPv6Address
    reason: BlockReason
    blocked_by: str
    block_note: Optional[str] = None
    blocked_until: Optional[datetime] = None
    permanently_blocked: bool
    is_active: bool


class BlockedIPListResponse(BaseModel):
    items: list[BlockedIPResponse]
    total: int
    limit: int
    offset: int


class BlockedIPCreateSchema(BaseModel):
    ip_address: IPv4Address | IPv6Address
    reason: BlockReason
    note: Optional[str] = None
    expires_in_minutes: Optional[int] = None
    permanently: bool = False