from sqlalchemy import Column, String, DateTime, ForeignKey, Float, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.common.models.base import Base

class SupplyItem(Base):
    __tablename__ = "supply_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Lien vers l'approvisionnement parent
    supply_id = Column(UUID(as_uuid=True), ForeignKey("supplies.id"), nullable=False)
    
    # Lien vers le produit concerné
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    
    # Détails de la ligne
    quantity = Column(Float, nullable=False) # Quantité reçue
    unit_price = Column(Float, nullable=False) # Prix d'achat unitaire au moment de l'approvisionnement
    
    # Traçabilité alimentaire (très important pour vous)
    batch_number = Column(String(100), index=True)
    expiry_date = Column(DateTime)
    
    # Relation inverse
    supply = relationship("Supply", back_populates="items")
    
    # Audit
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<SupplyItem(supply_id='{self.supply_id}', quantity={self.quantity})>"