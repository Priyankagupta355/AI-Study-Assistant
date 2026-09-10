from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database.database import Base


class StudyProgress(Base):

    __tablename__ = "study_progress"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    subject = Column(
        String,
        nullable=False
    )

    topic = Column(
        String,
        nullable=False
    )

    study_hours = Column(
        Float,
        default=0
    )

    quiz_score = Column(
        Float,
        default=0
    )

    status = Column(
        String,
        default="in_progress"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )