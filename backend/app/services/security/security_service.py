from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.security.blocked_ip import (
    BlockReason,
    BlockedIP,
)

from app.models.security.login_attempt import (
    AuthenticationFailureReason,
    AttemptType,
    LoginAttempt,
)

from app.models.security.security_event import (
    EventSeverity,
    SecurityEvent,
    SecurityEventType,
)

from app.repositories.security.blocked_ip_repository import (
    BlockedIPRepository,
)

from app.repositories.security.login_attempt_repository import (
    LoginAttemptRepository,
)

from app.repositories.security.request_log_repository import (
    RequestLogRepository,
)

from app.repositories.security.security_event_repository import (
    SecurityEventRepository,
)


class SecurityService:

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:

        self.db = db

        self.event_repo = SecurityEventRepository(db)

        self.request_log_repo = RequestLogRepository(db)

        self.login_attempt_repo = LoginAttemptRepository(db)

        self.blocked_ip_repo = BlockedIPRepository(db)

    # ---------------------------------------------------------
    # Login Attempts
    # ---------------------------------------------------------

    async def record_login_attempt(
        self,
        *,
        email: str,
        ip_address: str,
        user_agent: str,
        successful: bool,
        customer_id: UUID | None = None,
        failure_reason: AuthenticationFailureReason | None = None,
        request_id: str | None = None,
    ) -> LoginAttempt:

        attempt = LoginAttempt(
            customer_id=customer_id,
            attempt_type=AttemptType.LOGIN,
            email=email,
            ip_address=ip_address,
            user_agent=user_agent,
            successful=successful,
            failure_reason=failure_reason,
            request_id=request_id,
        )

        await self.login_attempt_repo.create(
            attempt,
        )

        await self.db.commit()

        await self.db.refresh(
            attempt,
        )

        return attempt

    # ---------------------------------------------------------
    # Security Events
    # ---------------------------------------------------------

    async def list_events(
        self,
        severity: Optional[EventSeverity] = None,
        resolved: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[SecurityEvent]:

        events = await self.event_repo.get_recent(
            limit + offset,
        )

        if severity is not None:
            events = [
                event
                for event in events
                if event.severity == severity
            ]

        if resolved is not None:
            events = [
                event
                for event in events
                if event.resolved == resolved
            ]

        return events[offset : offset + limit]

    async def get_event_by_public_id(
        self,
        public_id: str,
    ) -> Optional[SecurityEvent]:

        return await self.event_repo.get_by_public_id(
            public_id,
        )

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

        await self.event_repo.create(
            event,
        )

        await self.db.commit()

        return event

    async def resolve_event(
        self,
        public_id: str,
    ) -> SecurityEvent:

        event = await self.event_repo.get_by_public_id(
            public_id,
        )

        if event is None:
            raise ValueError(
                "Security event not found."
            )

        event.resolved = True

        await self.event_repo.save(
            event,
        )

        await self.db.commit()

        return event

    # ---------------------------------------------------------
    # Blocked IPs
    # ---------------------------------------------------------

    async def block_ip(
        self,
        ip: str,
        reason: BlockReason,
        blocked_by: str = "system",
        note: Optional[str] = None,
        expires_in_minutes: Optional[int] = None,
        permanently: bool = False,
    ) -> BlockedIP:

        existing = (
            await self.blocked_ip_repo.get_by_ip_address(
                ip
            )
        )

        if existing and existing.is_active:
            raise ValueError(
                "IP is already blocked."
            )

        if existing:

            existing.is_active = True

            existing.reason = reason

            existing.blocked_by = blocked_by

            existing.block_note = note

            if permanently:

                existing.permanently_blocked = True

                existing.blocked_until = None

            else:

                existing.permanently_blocked = False

                existing.blocked_until = (
                    datetime.now(timezone.utc)
                    + timedelta(
                        minutes=expires_in_minutes or 60
                    )
                )

            await self.blocked_ip_repo.save(
                existing,
            )

            await self.db.commit()

            return existing

        blocked = BlockedIP(
            ip_address=ip,
            reason=reason,
            blocked_by=blocked_by,
            block_note=note,
            permanently_blocked=permanently,
            blocked_until=(
                None
                if permanently
                else datetime.now(timezone.utc)
                + timedelta(
                    minutes=expires_in_minutes or 60
                )
            ),
            is_active=True,
        )

        await self.blocked_ip_repo.create(
            blocked,
        )

        await self.db.commit()

        return blocked

    async def unblock_ip(
        self,
        public_id: str,
    ) -> None:

        blocked = (
            await self.blocked_ip_repo.get_by_public_id(
                public_id
            )
        )

        if blocked is None:
            raise ValueError(
                "Blocked IP not found."
            )

        blocked.is_active = False

        await self.blocked_ip_repo.save(
            blocked,
        )

        await self.db.commit()

    async def list_active_blocks(
        self,
    ) -> list[BlockedIP]:

        return (
            await self.blocked_ip_repo.list_active_blocks(
                datetime.now(timezone.utc)
            )
        )

    # ---------------------------------------------------------
    # Dashboard
    # ---------------------------------------------------------

    async def get_dashboard_stats(
        self,
    ) -> dict:

        now = datetime.now(timezone.utc)

        last_hour = now - timedelta(hours=1)

        last_24h = now - timedelta(days=1)

        total_requests = (
            await self.request_log_repo.count_requests()
        )

        requests_last_hour = (
            await self.request_log_repo.count_requests_since(
                last_hour
            )
        )

        total_security_events = (
            await self.event_repo.count_events()
        )

        critical_events = (
            await self.event_repo.count_by_severity(
                EventSeverity.CRITICAL
            )
        )

        high_events = (
            await self.event_repo.count_by_severity(
                EventSeverity.HIGH
            )
        )

        failed_logins_last_24h = (
            await self.login_attempt_repo.count_recent_failures(
                last_24h
            )
        )

        blocked_ips = (
            await self.blocked_ip_repo.count_active_blocks(
                now
            )
        )

        top_ips = await self._get_top_ips()

        return {
            "total_requests": total_requests,
            "requests_last_hour": requests_last_hour,
            "total_security_events": total_security_events,
            "critical_events": critical_events,
            "high_events": high_events,
            "failed_logins_last_24h": failed_logins_last_24h,
            "blocked_ips": blocked_ips,
            "top_ips": top_ips,
        }

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    async def _get_top_ips(
        self,
        limit: int = 10,
    ) -> list[dict]:

        rows = (
            await self.request_log_repo.get_top_ips(
                limit
            )
        )

        return [
            {
                "ip": ip,
                "count": count,
            }
            for ip, count in rows
        ]


# ---------------------------------------------------------
# Utility
# ---------------------------------------------------------

async def create_security_event_async(
    event_type: str,
    severity: str,
    title: str,
    description: str,
    ip: str,
    request_id: str | None = None,
    evidence: dict | None = None,
) -> None:

    from app.db.database import AsyncSessionLocal

    async with AsyncSessionLocal() as db:

        service = SecurityService(db)

        await service.create_event(
            event_type=SecurityEventType(event_type),
            severity=EventSeverity(severity),
            title=title,
            description=description,
            ip=ip,
            request_id=request_id,
            evidence=evidence,
        )