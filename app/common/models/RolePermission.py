from datetime import datetime
import uuid

from sqlalchemy import CHAR, JSON, UUID, Column, Float, ForeignKey, Integer, String, Boolean, DateTime, Text, func
from app.common.models.base import Base

class RolePermission(Base):
    __tablename__ = "role_permissions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4 , index=True)
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permissions.id"))
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"))
    
    state = Column(Integer , default=1)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
 
    