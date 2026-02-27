from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class ApplicationStatus(str, enum.Enum):
    APPLIED = "Applied"
    SCREENING = "Screening"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    HIRED = "Hired"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"


class Application(Base, TimestampMixin):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("candidate_id", "requisition_id", name="uq_applications_candidate_requisition"),
        Index("ix_applications_status", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    requisition_id: Mapped[int] = mapped_column(ForeignKey("requisitions.id"), nullable=False)
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, name="application_status"), nullable=False
    )

    candidate = relationship("Candidate", back_populates="applications")
    requisition = relationship("Requisition", back_populates="applications")
    status_audits = relationship("ApplicationStatusAudit", back_populates="application", cascade="all, delete-orphan")
    interview_feedback = relationship("InterviewFeedback", back_populates="application", cascade="all, delete-orphan")
    offer = relationship("Offer", back_populates="application", uselist=False, cascade="all, delete-orphan")


class ApplicationStatusAudit(Base, TimestampMixin):
    __tablename__ = "application_status_audits"
    __table_args__ = (Index("ix_application_status_audits_application_id", "application_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"), nullable=False)
    from_status: Mapped[ApplicationStatus | None] = mapped_column(
        Enum(ApplicationStatus, name="application_status"), nullable=True
    )
    to_status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, name="application_status"), nullable=False
    )
    changed_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    application = relationship("Application", back_populates="status_audits")
    changed_by_user = relationship("User", back_populates="changed_status_audits")
