from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user, require_roles
from app.db.session import get_db
from app.models.requisition import Requisition
from app.models.user import User, UserRole
from app.schemas.requisition import RequisitionCommentRequest, RequisitionCreate, RequisitionUpdate

router = APIRouter(prefix="/requisitions", tags=["requisitions"])


@router.post("", response_model=dict)
async def create_requisition(
    payload: RequisitionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.RECRUITER)),
) -> dict:
    requisition = Requisition(organization_id=current_user.organization_id, **payload.model_dump())
    db.add(requisition)
    await db.commit()
    await db.refresh(requisition)
    return {"id": requisition.id}


@router.put("/{requisition_id}")
async def edit_requisition(
    requisition_id: int,
    payload: RequisitionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.RECRUITER)),
) -> dict:
    result = await db.execute(
        select(Requisition).where(
            Requisition.id == requisition_id,
            Requisition.organization_id == current_user.organization_id,
            Requisition.deleted_at.is_(None),
        )
    )
    requisition = result.scalar_one_or_none()
    if not requisition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requisition not found")

    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(requisition, key, value)

    await db.commit()
    return {"status": "updated"}


@router.delete("/{requisition_id}/archive")
async def archive_requisition(
    requisition_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.RECRUITER)),
) -> dict:
    result = await db.execute(
        select(Requisition).where(
            Requisition.id == requisition_id,
            Requisition.organization_id == current_user.organization_id,
            Requisition.deleted_at.is_(None),
        )
    )
    requisition = result.scalar_one_or_none()
    if not requisition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requisition not found")

    requisition.deleted_at = datetime.now(timezone.utc)
    await db.commit()
    return {"status": "archived"}


@router.get("/{requisition_id}")
async def view_requisition(
    requisition_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.RECRUITER, UserRole.HIRING_MANAGER)),
) -> dict:
    result = await db.execute(
        select(Requisition).where(
            Requisition.id == requisition_id,
            Requisition.organization_id == current_user.organization_id,
            Requisition.deleted_at.is_(None),
        )
    )
    requisition = result.scalar_one_or_none()
    if not requisition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requisition not found")

    return {
        "id": requisition.id,
        "title": requisition.title,
        "department": requisition.department,
        "location": requisition.location,
        "employment_type": requisition.employment_type,
        "required_skills": requisition.required_skills,
        "status": requisition.status,
    }


@router.post("/{requisition_id}/comments")
async def comment_on_requisition(
    requisition_id: int,
    payload: RequisitionCommentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.RECRUITER, UserRole.HIRING_MANAGER)),
) -> dict:
    result = await db.execute(
        select(Requisition).where(
            Requisition.id == requisition_id,
            Requisition.organization_id == current_user.organization_id,
            Requisition.deleted_at.is_(None),
        )
    )
    requisition = result.scalar_one_or_none()
    if not requisition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requisition not found")

    return {"status": "comment added", "requisition_id": requisition_id, "comment": payload.comment}
