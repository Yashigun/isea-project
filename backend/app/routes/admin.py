from backend.app.models.security.security_event import EventSeverity
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.security.security_service import SecurityService
from app.schemas.security import (
    SecurityEventResponse,
    BlockedIPResponse,
    BlockedIPCreateSchema,
)
from app.core.dependencies import get_current_admin
from typing import List, Optional

router = APIRouter(prefix="/admin/security", tags=["admin-security"], dependencies=[Depends(get_current_admin)])

@router.get("/events", response_model=List[SecurityEventResponse])
async def list_events(
    severity: Optional[str] = None,
    resolved: Optional[bool] = None,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    service = SecurityService(db)
    # Convert severity string to enum if provided
    severity_enum = None
    if severity:
        try:
            severity_enum = EventSeverity(severity.lower())
        except ValueError:
            pass
    events = await service.list_events(severity_enum, resolved, limit, offset)
    return events

@router.post("/events/{public_id}/resolve")
async def resolve_event(public_id: str, db: AsyncSession = Depends(get_db)):
    service = SecurityService(db)
    try:
        event = await service.resolve_event(public_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Event resolved"}

@router.get("/dashboard/stats")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    service = SecurityService(db)
    stats = await service.get_dashboard_stats()
    return stats

@router.get("/blocked-ips", response_model=List[BlockedIPResponse])
async def list_blocked_ips(db: AsyncSession = Depends(get_db)):
    service = SecurityService(db)
    blocks = await service.list_active_blocks()
    return blocks

@router.post("/blocked-ips", response_model=BlockedIPResponse)
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
async def unblock_ip(public_id: str, db: AsyncSession = Depends(get_db)):
    service = SecurityService(db)
    try:
        await service.unblock_ip(public_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "IP unblocked"}