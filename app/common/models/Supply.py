from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.common.models.base import Base

class Supply(Base):
    __tablename__ = "supplies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Référence interne (ex: APP-2026-001)
    reference_number = Column(String(100), unique=True, index=True, nullable=False)
    
    # Origine du stock
    supplier_name = Column(String(255)) 
    # Optionnel : foreign_key vers une table 'suppliers' si vous en avez une
    
    # Informations financières globales
    total_cost = Column(Float, default=0.0)
    currency = Column(String(3), default="XAF")
    
    # Logistique
    supply_date = Column(DateTime(timezone=True), server_default=func.now())
    received_by = Column(String(100)) # Nom de la personne qui a réceptionné
    notes = Column(Text)
    status = Column(String(50), default="received") # ordered, received, cancelled

    # Relation vers les articles (pour accéder facilement aux lignes depuis l'entête)
    items = relationship("SupplyItem", back_populates="supply", cascade="all, delete-orphan")

    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    # Audit
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<Supply(ref='{self.reference_number}', total='{self.total_cost}')>"