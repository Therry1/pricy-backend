from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.common.models.base import Base

class ProductStock(Base):
    __tablename__ = "product_stocks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 1. Liens (Foreign Keys)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False, index=True)
    # Si vous avez plusieurs dépôts ou boutiques (ex: Magasin Ngaoundéré, Dépôt Centre)
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"), nullable=True)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=True)

    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    
    # 2. Quantités
    current_quantity = Column(Float, default=0.0, nullable=False)
    minimum_threshold = Column(Float, default=5.0) # Seuil d'alerte de stock bas
    reserved_quantity = Column(Float, default=0.0) # Articles commandés mais pas encore sortis

    is_kit = Column(Boolean , default=False)
    # 3. Traçabilité Alimentaire & Industrielle
    # On indexe le lot pour des recherches rapides en cas de rappel produit
    batch_number = Column(String(100), index=True) 
    expiry_date = Column(DateTime, index=True) # Très important pour le FEFO (First Expired, First Out)
    
    # 4. Localisation précise dans le dépôt
    aisle = Column(String(50)) # Allée
    shelf = Column(String(50)) # Étagère
    bin_location = Column(String(50)) # Casier

    # 5. Audit
    last_stock_count = Column(DateTime) # Date du dernier inventaire physique
    
    
    # Audit
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relation inverse
    warehouse = relationship("Warehouse", back_populates="stocks")
    location = relationship("Location", back_populates="stocks")
    
    
    # Relations
    product = relationship("Product", back_populates="stocks")

    def __repr__(self):
        return f"<ProductStock(product_id='{self.product_id}', qty={self.current_quantity}, batch='{self.batch_number}')>"