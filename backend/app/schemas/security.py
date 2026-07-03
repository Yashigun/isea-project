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