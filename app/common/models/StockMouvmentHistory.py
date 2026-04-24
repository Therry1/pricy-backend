from sqlalchemy import UUID, Column, Integer, String, Enum, Float, ForeignKey, DateTime
from datetime import datetime

from app.common.configs.global_constants import EntityType
from app.common.models.base import Base

class StockMovementHistory(Base):
    __tablename__ = "stock_movement_histories"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    stock_id = Column(UUID(as_uuid=True), ForeignKey("product_stocks.id"), nullable=False)
    
    old_quantity = Column(Float, nullable=False)
    new_quantity = Column(Float, nullable=False)
    change_amount = Column(Float, nullable=False) # Quantité ajoutée ou retirée
    
    # --- LOGIQUE POLYMORPHE ---
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    
    # Provenance
    origin_id = Column(UUID(as_uuid=True), nullable=True) # ID de l'entrepôt ou du PDV
    origin_type = Column(Enum(EntityType), nullable=True)
    
    # Destination
    destination_id = Column(UUID(as_uuid=True), nullable=True) # ID de l'entrepôt ou du PDV
    destination_type = Column(Enum(EntityType), nullable=True)
    
    reason = Column(String, nullable=True) # Ex: "Vente #45", "Réception"
    created_at = Column(DateTime, default=datetime.utcnow)