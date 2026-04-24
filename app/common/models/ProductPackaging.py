from datetime import datetime
import uuid

from sqlalchemy import CHAR, JSON, UUID, Column, Float, ForeignKey, Integer, String, Boolean, DateTime, Text, func
from app.common.models.base import Base



class Packaging(Base):
    __tablename__ = "product_packagings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # --- Informations sur le type de conditionnement ---
    # ex: 'Box', 'Blister pack', 'Carton', 'Tray'
    packaging_name = Column(String(100), nullable=False, unique=True) 
    
    # Description technique (ex: 'Alvéole plastique pour 12 œufs')
    packaging_description = Column(Text)
    
    # Matériau principal (ex: 'Cardboard', 'PVC', 'Aluminum')
    packaging_material = Column(String(100))
    
    # --- Logistique & Recyclage ---
    is_recyclable = Column(Boolean, default=True)
    is_returnable = Column(Boolean, default=False)  # Si l'emballage est consigné
    
    # Capacité standard (ex: combien d'unités ce conditionnement contient par défaut)
    standard_capacity = Column(Integer, default=1)

    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    # Audit
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<Packaging(name='{self.packaging_name}', material='{self.packaging_material}')>"