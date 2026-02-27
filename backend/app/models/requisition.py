from __future__ import annotations

import enum

from sqlalchemy import JSON, Enum, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin


class EmploymentType(str, enum.Enum):
    FULL_TIME = "FullTime"
    PART_TIME = "PartTime"
    CONTRACT = "Contract"
    TEMPORARY = "Temporary"
    INTERN = "Intern"


class RequisitionStatus(str, enum.Enum):
    DRAFT = "Draft"
    OPEN = "Open"
    ON_HOLD = "OnHold"
    CLOSED = "Closed"
    CANCELLED = "Cancelled"


class Requisition(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "requisitions"
    __table_args__ = (
        Index("ix_requisitions_organization_id", "organization_id"),
        Index("ix_requisitions_status", "status"),
        Index("ix_requisitions_title", "title"),
        Index("ix_requisitions_department", "department"),
        Index("ix_requisitions_location", "location"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    hiring_manager_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    employment_type: Mapped[EmploymentType] = mapped_column(
        Enum(EmploymentType, name="employment_type"), nullable=False
    )
    required_skills: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[RequisitionStatus] = mapped_column(
        Enum(RequisitionStatus, name="requisition_status"), nullable=False
    )

    organization = relationship("Organization", back_populates="requisitions")
    hiring_manager = relationship("User", back_populates="managed_requisitions")
    applications = relationship("Application", back_populates="requisition", cascade="all, delete-orphan")
    interview_stages = relationship("InterviewStage", back_populates="requisition", cascade="all, delete-orphan")
