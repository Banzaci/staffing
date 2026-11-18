
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class WorkerWorkAuthorization(Base):
    __tablename__ = "worker_work_authorizations"

    __table_args__ = (
        UniqueConstraint(
            "worker_profile_id",
            "country_code",
            "authorization_type",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    worker_profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("worker_profiles.id"),
        nullable=False,
    )

    country_code: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
    )

    authorization_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    expires_at: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    verification_status: Mapped[str] = mapped_column(
        String(20),
        default="unverified",
        nullable=False,
    )

    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
