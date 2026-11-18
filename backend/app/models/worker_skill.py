
import uuid

from sqlalchemy import ForeignKey, Integer, UniqueConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class WorkerSkill(Base):
    __tablename__ = "worker_skills"

    __table_args__ = (
        UniqueConstraint("worker_profile_id", "skill_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    worker_profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("worker_profiles.id"),
        nullable=False,
    )

    skill_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("skills.id"),
        nullable=False,
    )

    years_experience: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    min_hourly_rate: Mapped[float | None] = mapped_column(
        Numeric(10, 2, asdecimal=False),
        nullable=True,
    )

    max_hourly_rate: Mapped[float | None] = mapped_column(
        Numeric(10, 2, asdecimal=False),
        nullable=True,
    )
