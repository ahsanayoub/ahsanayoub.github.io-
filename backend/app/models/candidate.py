from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin


class Candidate(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "candidates"
    __table_args__ = (
        Index("ix_candidates_organization_id", "organization_id"),
        Index("ix_candidates_email", "email"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    current_company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    current_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    years_experience: Mapped[int | None] = mapped_column(nullable=True)

    resume_file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resume_file_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    resume_uploaded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    parsed_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    parsed_skills: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    parsed_education: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)
    parsed_experience: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)

    organization = relationship("Organization", back_populates="candidates")
    applications = relationship("Application", back_populates="candidate", cascade="all, delete-orphan")
