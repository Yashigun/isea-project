from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime
from app.models.security.security_event import EventSeverity, SecurityEventType
from app.models.security.blocked_ip import BlockReason


class SecurityEventResponse(BaseModel):
    public_id: str
    event_type: SecurityEventType
    severity: EventSeverity
    title: str
    description: str
    ip_address: str
    country: Optional[str] = None
    city: Optional[str] = None
    resolved: bool
    created_at: datetime
    evidence: Optional[dict] = None

class BlockedIPResponse(BaseModel):
    public_id: str
    ip_address: str
    reason: BlockReason
    blocked_by: str
    block_note: Optional[str] = None
    blocked_until: Optional[datetime] = None
    permanently_blocked: bool
    is_active: bool
    created_at: datetime

class BlockedIPCreateSchema(BaseModel):
    ip_address: str
    reason: BlockReason
    note: Optional[str] = None
    expires_in_minutes: Optional[int] = None
    permanently: bool = False
    
# ... existing imports

class RequestLogResponse(BaseModel):
    public_id: str
    method: str
    route: str
    path: str
    query_string: Optional[str] = None
    status_code: int
    response_time_ms: int
    ip_address: str
    user_agent: str
    country: Optional[str] = None
    city: Optional[str] = None
    created_at: datetime
    customer_id: Optional[str] = None

class LoginAttemptResponse(BaseModel):
    public_id: str
    email: str
    ip_address: str
    user_agent: str
    successful: bool
    failure_reason: Optional[str] = None
    attempt_type: str
    created_at: datetime
    customer_id: Optional[str] = None

class AuditLogResponse(BaseModel):
    public_id: str
    action: str
    entity_type: str
    entity_name: Optional[str] = None
    entity_public_id: Optional[str] = None
    old_data: Optional[dict] = None
    new_data: Optional[dict] = None
    ip_address: str
    user_agent: str
    created_at: datetime
    customer_id: Optional[str] = None

class BlockedIPResponse(BaseModel):
    public_id: str
    ip_address: str
    reason: str
    blocked_by: str
    block_note: Optional[str] = None
    blocked_until: Optional[datetime] = None
    permanently_blocked: bool
    is_active: bool
    created_at: datetime