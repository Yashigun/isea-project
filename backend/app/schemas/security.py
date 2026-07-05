from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from typing import Optional

from app.models.security.request_log import HttpMethod
from pydantic import BaseModel, ConfigDict

from app.models.security.security_event import (
    EventSeverity,
    SecurityEventType,
)
from uuid import UUID
from app.models.security.blocked_ip import BlockReason

from app.models.security.login_attempt import (
    AttemptType,
    AuthenticationFailureReason
)
from app.models.security.audit_log import (
    AuditAction,
    EntityType,
)
from app.models.security.request_log import (
    HttpMethod,
    HttpProtocol,
    RequestSource,
    RequestOutcome,
)

from ipaddress import IPv4Address, IPv6Address

# -------------------------------------------------------
# Security Events
# -------------------------------------------------------

class SecurityEventResponse(BaseModel):
    public_id: str
    event_type: SecurityEventType
    severity: EventSeverity
    title: str
    description: str
    ip_address: IPv4Address | IPv6Address
    country: Optional[str] = None
    city: Optional[str] = None
    resolved: bool
    created_at: datetime
    evidence: Optional[dict] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# -------------------------------------------------------
# Request Logs
# -------------------------------------------------------



class RequestLogResponse(BaseModel):
    public_id: str
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
    created_at: datetime
    customer_id: UUID | None = None
    model_config = ConfigDict(
        from_attributes=True
    )


class RequestLogListResponse(BaseModel):
    items: list[RequestLogResponse]
    total: int
    limit: int
    offset: int


# -------------------------------------------------------
# Login Attempts
# -------------------------------------------------------

class LoginAttemptResponse(BaseModel):
    public_id: str
    email: str
    ip_address: IPv4Address | IPv6Address
    user_agent: str
    successful: bool
    failure_reason: AuthenticationFailureReason | None = None
    attempt_type: AttemptType
    created_at: datetime
    customer_id: UUID | None = None

    model_config = ConfigDict(
        from_attributes=True
    )

class LoginAttemptListResponse(BaseModel):
    items: list[LoginAttemptResponse]
    total: int
    limit: int
    offset: int


# -------------------------------------------------------
# Audit Logs
# -------------------------------------------------------



class AuditLogResponse(BaseModel):
    public_id: str
    action: AuditAction
    entity_type: EntityType
    entity_name: str | None = None
    entity_public_id: str | None = None
    old_data: dict | None = None
    new_data: dict | None = None
    ip_address: IPv4Address | IPv6Address
    user_agent: str
    created_at: datetime
    customer_id: UUID | None = None
    model_config = ConfigDict(
        from_attributes=True
    )

class AuditLogListResponse(BaseModel):
    items: list[AuditLogResponse]
    total: int
    limit: int
    offset: int


# -------------------------------------------------------
# Blocked IPs
# -------------------------------------------------------

class BlockedIPResponse(BaseModel):
    public_id: str
    ip_address: IPv4Address | IPv6Address
    reason: BlockReason
    blocked_by: str
    block_note: Optional[str] = None
    blocked_until: Optional[datetime] = None
    permanently_blocked: bool
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


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