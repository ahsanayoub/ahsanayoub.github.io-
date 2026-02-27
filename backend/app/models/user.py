from __future__ import annotations

import enum

from sqlalchemy import Enum, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class UserRole(str, enum.Enum):
    ADMIN = "Admin"
    RECRUITER = "Recruiter"
    HIRING_MANAGER = "HiringManager"


class User(Base, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_organization_id", "organization_id"),
        Index("ix_users_role", "role"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    organization = relationship("Organization", back_populates="users")
    managed_requisitions = relationship("Requisition", back_populates="hiring_manager")
    changed_status_audits = relationship("ApplicationStatusAudit", back_populates="changed_by_user")
    interview_feedback = relationship("InterviewFeedback", back_populates="interviewer")
