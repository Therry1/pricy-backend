from sqlalchemy import Column, Float, ForeignKey, String, Boolean, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.common.models.base import Base

class Location(Base):
    __tablename__ = "locations"

    # 1. Identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), nullable=False, unique=True) # ex: "Main Warehouse", "Cold Storage"
    code = Column(String(20), unique=True, index=True)      # ex: "WH-01", "NGA-DEPOT"
    
    # 2. Location & Contact
    address = Column(Text)
    city = Column(String(100))      # ex: "Ngaoundéré"
    phone_number = Column(String(50))
    manager_name = Column(String(100)) # Responsable de l'entrepôt
    
    # 3. Technical Specifications
    warehouse_type = Column(String, nullable=False)
    is_cold_storage = Column(Boolean, default=False) # Important pour l'alimentaire (produits frais)
    capacity_m3 = Column(Float, nullable=True)       # Capacité en mètres cubes
    is_active = Column(Boolean, default=True)
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    # Audit
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relations
    # Permet de voir tous les stocks contenus dans ce point de vent
    stocks = relationship("ProductStock", back_populates="location")

    def __repr__(self):
        return f"<Warehouse(name='{self.name}', city='{self.city}', cold='{self.is_cold_storage}')>"