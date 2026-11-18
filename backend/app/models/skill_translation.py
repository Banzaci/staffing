
import uuid

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class SkillTranslation(Base):
    __tablename__ = "skill_translations"

    __table_args__ = (
        UniqueConstraint("skill_id", "language_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    skill_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("skills.id"),
        nullable=False,
    )

    language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
