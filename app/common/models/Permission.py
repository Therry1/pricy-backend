from datetime import datetime
import uuid

from sqlalchemy import CHAR, JSON, UUID, Column, Float, ForeignKey, Integer, String, Boolean, DateTime, Text, func
from app.common.models.base import Base

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    label = Column(String(50), unique=True, index=True, nullable=False)
    code = Column(String(15), unique=True, index=True, nullable=False)
    description = Column(String(150), nullable=True)
    
    code_module = Column(String(10), nullable=False)
    state = Column(Integer , default=1)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    