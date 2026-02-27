from __future__ import annotations

import enum

from sqlalchemy import Enum, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Recommendation(str, enum.Enum):
    STRONG_YES = "StrongYes"
    YES = "Yes"
    NO = "No"
    STRONG_NO = "StrongNo"


class InterviewStage(Base, TimestampMixin):
    __tablename__ = "interview_stages"
    __table_args__ = (
        Index("ix_interview_stages_requisition_id", "requisition_id"),
        Index("ix_interview_stages_stage_order", "stage_order"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    requisition_id: Mapped[int] = mapped_column(ForeignKey("requisitions.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    stage_order: Mapped[int] = mapped_column(Integer, nullable=False)
    is_required: Mapped[bool] = mapped_column(default=True, nullable=False)

    requisition = relationship("Requisition", back_populates="interview_stages")
    feedback = relationship("InterviewFeedback", back_populates="interview_stage", cascade="all, delete-orphan")


class InterviewFeedback(Base, TimestampMixin):
    __tablename__ = "interview_feedback"
    __table_args__ = (
        Index("ix_interview_feedback_application_id", "application_id"),
        Index("ix_interview_feedback_interview_stage_id", "interview_stage_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"), nullable=False)
    interview_stage_id: Mapped[int] = mapped_column(ForeignKey("interview_stages.id"), nullable=False)
    interviewer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comments: Mapped[str | None] = mapped_column(String(4000), nullable=True)
    recommendation: Mapped[Recommendation] = mapped_column(
        Enum(Recommendation, name="interview_recommendation"), nullable=False
    )

    application = relationship("Application", back_populates="interview_feedback")
    interview_stage = relationship("InterviewStage", back_populates="feedback")
    interviewer = relationship("User", back_populates="interview_feedback")
