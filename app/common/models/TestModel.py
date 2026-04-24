from datetime import datetime
import uuid

from sqlalchemy import UUID, Column, Integer, String, Boolean, DateTime, func
from app.common.models.base import Base


class TestModel(Base):
    __tablename__ = "test_models"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4  # ← fonction passée comme default, pas comme type
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)