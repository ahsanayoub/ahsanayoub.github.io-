from __future__ import annotations

from pydantic import BaseModel

from app.models.requisition import EmploymentType, RequisitionStatus


class RequisitionCreate(BaseModel):
    hiring_manager_id: int
    title: str
    department: str
    location: str
    employment_type: EmploymentType
    required_skills: list[str]
    status: RequisitionStatus


class RequisitionUpdate(BaseModel):
    title: str | None = None
    department: str | None = None
    location: str | None = None
    employment_type: EmploymentType | None = None
    required_skills: list[str] | None = None
    status: RequisitionStatus | None = None


class RequisitionCommentRequest(BaseModel):
    comment: str
