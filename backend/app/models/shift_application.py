
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Index, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ShiftApplication(Base):
    __tablename__ = "shift_applications"

    __table_args__ = (
        Index(
            "uq_active_shift_application",
            "job_shift_id",
            "worker_profile_id",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    job_shift_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("job_shifts.id"),
        nullable=False,
    )

    worker_profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("worker_profiles.id"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
