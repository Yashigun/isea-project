from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.dependencies import get_current_admin
from app.models.store.customer import Customer
from app.models.security.security_event import EventSeverity, SecurityEventType
from app.models.security.blocked_ip import BlockReason, BlockedIP
from app.models.security.login_attempt import LoginAttempt
from app.models.security.request_log import RequestLog
from app.schemas.security import (
    SecurityEventResponse,
    BlockedIPResponse,
    BlockedIPCreateSchema,
    RequestLogResponse,
    LoginAttemptResponse,
    AuditLogResponse,
    RequestLogListResponse,
    LoginAttemptListResponse,
    AuditLogListResponse,
    BlockedIPListResponse,
    CustomerSessionListResponse,
    CustomerSessionResponse,
)
from app.services.security.security_service import SecurityService
from app.repositories.security.request_log_repository import RequestLogRepository
from app.repositories.security.login_attempt_repository import LoginAttemptRepository
from app.repositories.security.audit_log_repository import AuditLogRepository
from app.repositories.security.blocked_ip_repository import BlockedIPRepository
from app.repositories.security.security_event_repository import SecurityEventRepository

router = APIRouter(prefix="/admin/security", tags=["admin-security"], dependencies=[Depends(get_current_admin)])

# ----------------------------------------
# Security Events
# ----------------------------------------

@router.get("/events", response_model=list[SecurityEventResponse])
async def list_security_events(
    severity: Optional[str] = Query(None),
    resolved: Optional[bool] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    service = SecurityService(db)
    events = await service.list_events(severity, resolved, limit)
    return events

@router.post("/events/{public_id}/resolve")
async def resolve_security_event(
    public_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = SecurityService(db)
    try:
        event = await service.resolve_event(public_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Event resolved"}

# ----------------------------------------
# Request Logs
# ----------------------------------------

@router.get("/requests",response_model=RequestLogListResponse)
async def get_request_logs(
    method: Optional[str] = Query(None),
    status_code: Optional[int] = Query(None),
    ip: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    repo = RequestLogRepository(db)
    logs, total = await repo.filter_logs(
        method=method,
        status_code=status_code,
        ip=ip,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset
    )
    return {
        "items": logs,
        "total": total,
        "limit": limit,
        "offset": offset,
    }

# ----------------------------------------
# Login Attempts
# ----------------------------------------

@router.get("/login-attempts",response_model=LoginAttemptListResponse)
async def get_login_attempts(
    email: Optional[str] = Query(None),
    ip: Optional[str] = Query(None),
    successful: Optional[bool] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    repo = LoginAttemptRepository(db)
    attempts, total = await repo.filter_attempts(
        email=email,
        ip=ip,
        successful=successful,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset
    )
    return {
        "items": attempts,
        "total": total,
        "limit": limit,
        "offset": offset,
    }

# ----------------------------------------
# Customer Sessions
# ----------------------------------------

@router.get(
    "/sessions",
    response_model=CustomerSessionListResponse,
)
async def list_customer_sessions(
    limit: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    db: AsyncSession = Depends(get_db),
):
    service = SecurityService(db)

    sessions, total = await service.list_customer_sessions(
        limit=limit,
        offset=offset,
    )

    return CustomerSessionListResponse(
        items=sessions,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/sessions/{public_id}",
    response_model=CustomerSessionResponse,
)
async def get_customer_session(
    public_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = SecurityService(db)

    try:
        return await service.get_customer_session(
            public_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.post(
    "/sessions/{public_id}/revoke",
    response_model=CustomerSessionResponse,
)
async def revoke_customer_session(
    public_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = SecurityService(db)

    try:
        return await service.revoke_customer_session(
            public_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

# ----------------------------------------
# Audit Logs
# ----------------------------------------

@router.get("/audit-logs", response_model=AuditLogListResponse)
async def get_audit_logs(
    action: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None),
    customer_id: Optional[UUID] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    repo = AuditLogRepository(db)
    logs, total = await repo.filter_logs(
        action=action,
        entity_type=entity_type,
        customer_id=customer_id,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset
    )
    return {
        "items": logs,
        "total": total,
        "limit": limit,
        "offset": offset,
    }

# ----------------------------------------
# Blocked IPs
# ----------------------------------------

@router.get("/blocked-ips", response_model=BlockedIPListResponse)
async def get_blocked_ips(
    active_only: bool = Query(False),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    repo = BlockedIPRepository(db)
    if active_only:
        items = await repo.list_active_blocks(datetime.now(timezone.utc))
        total = len(items)
        items = items[offset:offset+limit]
    else:
        stmt = select(BlockedIP).order_by(BlockedIP.created_at.desc()).offset(offset).limit(limit)
        result = await db.execute(stmt)
        items = result.scalars().all()
        total_stmt = select(func.count(BlockedIP.id))
        total = await db.scalar(total_stmt) or 0
    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }

@router.post( "/blocked-ips", response_model=BlockedIPResponse)
async def block_ip(
    data: BlockedIPCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    service = SecurityService(db)
    try:
        blocked = await service.block_ip(
            ip=data.ip_address,
            reason=data.reason,
            note=data.note,
            expires_in_minutes=data.expires_in_minutes,
            permanently=data.permanently,
            blocked_by="admin",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return blocked

@router.delete("/blocked-ips/{public_id}")
async def unblock_ip(
    public_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = SecurityService(db)
    try:
        await service.unblock_ip(public_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "IP unblocked"}

# ----------------------------------------
# Statistics
# ----------------------------------------

@router.get("/dashboard/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
):
    service = SecurityService(db)
    return await service.get_dashboard_stats()

@router.get("/stats/requests-by-ip")
async def get_requests_by_ip(
    since: Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    if not since:
        since = datetime.now(timezone.utc) - timedelta(days=1)
    repo = RequestLogRepository(db)
    stmt = (
        select(RequestLog.ip_address, func.count(RequestLog.id))
        .where(RequestLog.created_at >= since)
        .group_by(RequestLog.ip_address)
        .order_by(func.count(RequestLog.id).desc())
        .limit(20)
    )
    result = await db.execute(stmt)
    return [{"ip": ip, "count": count} for ip, count in result.all()]

@router.get("/stats/failed-logins-by-ip")
async def get_failed_logins_by_ip(
    since: Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    if not since:
        since = datetime.now(timezone.utc) - timedelta(days=1)
    stmt = (
        select(LoginAttempt.ip_address, func.count(LoginAttempt.id))
        .where(LoginAttempt.successful.is_(False))
        .where(LoginAttempt.created_at >= since)
        .group_by(LoginAttempt.ip_address)
        .order_by(func.count(LoginAttempt.id).desc())
        .limit(20)
    )
    result = await db.execute(stmt)
    return [{"ip": ip, "count": count} for ip, count in result.all()]