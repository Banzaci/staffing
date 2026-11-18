
import uuid

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class WorkerLanguage(Base):
    __tablename__ = "worker_languages"

    __table_args__ = (
        UniqueConstraint("worker_profile_id", "language_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    worker_profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("worker_profiles.id"),
        nullable=False,
    )

    language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
        nullable=False,
    )

    proficiency: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
