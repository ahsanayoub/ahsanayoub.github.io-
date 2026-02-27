from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    requisitions = relationship("Requisition", back_populates="organization", cascade="all, delete-orphan")
    candidates = relationship("Candidate", back_populates="organization", cascade="all, delete-orphan")
