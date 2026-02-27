from __future__ import annotations

import enum

from sqlalchemy import Enum, ForeignKey, Index, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class OfferStatus(str, enum.Enum):
    DRAFT = "Draft"
    EXTENDED = "Extended"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    EXPIRED = "Expired"


class Offer(Base, TimestampMixin):
    __tablename__ = "offers"
    __table_args__ = (
        Index("ix_offers_status", "status"),
        Index("ix_offers_application_id", "application_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"), nullable=False, unique=True)
    base_salary: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    bonus: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    equity: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    status: Mapped[OfferStatus] = mapped_column(Enum(OfferStatus, name="offer_status"), nullable=False)

    application = relationship("Application", back_populates="offer")
