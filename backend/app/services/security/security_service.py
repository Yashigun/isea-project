from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from uuid import UUID
from app.models.security.request_log import RequestLog
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.repositories.security.security_event_repository import SecurityEventRepository
from app.repositories.security.request_log_repository import RequestLogRepository
from app.repositories.security.blocked_ip_repository import BlockedIPRepository
from app.repositories.security.login_attempt_repository import LoginAttemptRepository
from app.models.security.security_event import SecurityEvent, SecurityEventType, EventSeverity
from app.models.security.blocked_ip import BlockedIP, BlockReason


class SecurityService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.event_repo = SecurityEventRepository(db)
        self.request_log_repo = RequestLogRepository(db)
        self.blocked_ip_repo = BlockedIPRepository(db)
        self.login_attempt_repo = LoginAttemptRepository(db)

    # ---- Events ----
    async def list_events(
        self,
        severity: Optional[EventSeverity] = None,
        resolved: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[SecurityEvent]:
        # For simplicity, we fetch recent and filter
        # In production, add proper filtering to the repository
        events = await self.event_repo.get_recent(limit + offset)
        if severity:
            events = [e for e in events if e.severity == severity]
        if resolved is not None:
            events = [e for e in events if e.resolved == resolved]
        return events[offset:offset+limit]

    async def get_event_by_public_id(self, public_id: str) -> Optional[SecurityEvent]:
        return await self.event_repo.get_by_public_id(public_id)

    async def create_event(
        self,
        event_type: SecurityEventType,
        severity: EventSeverity,
        title: str,
        description: str,
        ip: str,
        customer_id: Optional[UUID] = None,
        session_id: Optional[UUID] = None,
        request_id: Optional[str] = None,
        evidence: Optional[dict] = None,
    ) -> SecurityEvent:
        event = SecurityEvent(
            request_id=request_id,
            customer_id=customer_id,
            session_id=session_id,
            event_type=event_type,
            severity=severity,
            title=title,
            description=description,
            ip_address=ip,
            evidence=evidence,
            resolved=False,
        )
        await self.event_repo.create(event)
        await self.db.commit()
        return event

    async def resolve_event(self, public_id: str) -> SecurityEvent:
        event = await self.event_repo.get_by_public_id(public_id)
        if not event:
            raise ValueError("Event not found")
        event.resolved = True
        await self.event_repo.save(event)
        await self.db.commit()
        return event

    # ---- Blocked IPs ----
    async def block_ip(
        self,
        ip: str,
        reason: BlockReason,
        blocked_by: str = "system",
        note: Optional[str] = None,
        expires_in_minutes: Optional[int] = None,
        permanently: bool = False,
    ) -> BlockedIP:
        existing = await self.blocked_ip_repo.get_by_ip_address(ip)
        if existing and existing.is_active:
            raise ValueError("IP already blocked")
        if existing and not existing.is_active:
            # Reactivate
            existing.is_active = True
            existing.reason = reason
            existing.blocked_by = blocked_by
            existing.block_note = note
            if permanently:
                existing.blocked_until = None
                existing.permanently_blocked = True
            else:
                existing.permanently_blocked = False
                existing.blocked_until = datetime.utcnow() + timedelta(minutes=expires_in_minutes or 60)
            await self.blocked_ip_repo.save(existing)
            await self.db.commit()
            return existing
        # New block
        blocked = BlockedIP(
            ip_address=ip,
            reason=reason,
            blocked_by=blocked_by,
            block_note=note,
            blocked_until=None if permanently else datetime.utcnow() + timedelta(minutes=expires_in_minutes or 60),
            permanently_blocked=permanently,
            is_active=True,
        )
        await self.blocked_ip_repo.create(blocked)
        await self.db.commit()
        return blocked

    async def unblock_ip(self, public_id: str) -> None:
        blocked = await self.blocked_ip_repo.get_by_public_id(public_id)
        if not blocked:
            raise ValueError("Blocked IP not found")
        blocked.is_active = False
        await self.blocked_ip_repo.save(blocked)
        await self.db.commit()

    async def list_active_blocks(self) -> List[BlockedIP]:
        now = datetime.utcnow()
        return await self.blocked_ip_repo.list_active_blocks(now)

    # ---- Dashboard Stats ----
    async def get_dashboard_stats(self) -> Dict[str, Any]:
        now = datetime.utcnow()
        last_hour = now - timedelta(hours=1)
        last_24h = now - timedelta(days=1)

        # Count requests (need custom method in RequestLogRepository to count all)
        total_requests = await self.request_log_repo.count_requests()
        requests_last_hour = await self._count_requests_since(last_hour)

        # Security events
        total_events = await self.event_repo.count_events()
        critical_events = await self.event_repo.count_by_severity(EventSeverity.CRITICAL)
        high_events = await self.event_repo.count_by_severity(EventSeverity.HIGH)

        # Failed logins
        failed_logins_last_24h = await self.login_attempt_repo.count_recent_failures("", last_24h)  # need to fix to count all

        # Blocked IPs
        active_blocks = await self.blocked_ip_repo.count_active_blocks(now)

        # Top IPs by requests (we need to add method to RequestLogRepository)
        top_ips = await self._get_top_ips(limit=10)

        return {
            "total_requests": total_requests,
            "requests_last_hour": requests_last_hour,
            "total_security_events": total_events,
            "critical_events": critical_events,
            "high_events": high_events,
            "failed_logins_last_24h": failed_logins_last_24h,
            "active_blocked_ips": active_blocks,
            "top_ips": top_ips,
        }

    # ---- Helper methods ----
    async def _count_requests_since(self, since: datetime) -> int:
        # We need to add this to RequestLogRepository
        stmt = select(func.count(RequestLog.id)).where(RequestLog.created_at >= since)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def _get_top_ips(self, limit: int = 10) -> List[Dict[str, Any]]:
        # Group by ip_address and count
        stmt = (
            select(RequestLog.ip_address, func.count(RequestLog.id))
            .group_by(RequestLog.ip_address)
            .order_by(func.count(RequestLog.id).desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        rows = result.all()
        return [{"ip": row[0], "count": row[1]} for row in rows]
    

async def create_security_event_async(
    event_type: str,
    severity: str,
    title: str,
    description: str,
    ip: str,
    request_id: Optional[str] = None,
    evidence: Optional[dict] = None,
) -> None:
    from app.db.database import AsyncSessionLocal
    from app.models.security.security_event import SecurityEventType, EventSeverity
    from app.repositories.security.security_event_repository import SecurityEventRepository

    async with AsyncSessionLocal() as db:
        repo = SecurityEventRepository(db)
        event = SecurityEvent(
            request_id=request_id,
            event_type=SecurityEventType(event_type),
            severity=EventSeverity(severity),
            title=title,
            description=description,
            ip_address=ip,
            evidence=evidence,
            resolved=False,
        )
        await repo.create(event)
        await db.commit()