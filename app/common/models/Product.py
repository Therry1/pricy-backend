from datetime import datetime
import uuid

from sqlalchemy import CHAR, JSON, UUID, Column, Float, ForeignKey, Integer, String, Boolean, DateTime, Text, func
from sqlalchemy.orm import relationship
from app.common.models.base import Base



class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = Column(String(255), nullable=False)
    
    # --- Spécificités Alimentaires ---
    allergens = Column(JSON) # ex: ["nuts", "milk"]
    nutrition_facts = Column(JSON) # Stocke calories, lipides, etc.
    
    # Dates critiques
    expiration_date = Column(DateTime)
    supply_threshold = Column(Integer , nullable=False)
    supply_threshold = Column(Integer , nullable=False)
    critical_threshold = Column(Integer , nullable=False)
    
    # Conservation & Physique
    weight_unit = Column(String(10), default="kg")
    storage_instructions = Column(String(255)) # ex: "Keep refrigerated"
    
    # Commercial
    unit_price = Column(Float, nullable=False)
    status = Column(String(50), default="available") # available, recalled, out_of_stock
    state = Column(Integer , default=1)
    # Relation
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    packaging_id = Column(UUID(as_uuid=True), ForeignKey("product_packagings.id"))

    # Audit
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    stocks = relationship("ProductStock", back_populates="product")
    
    def __repr__(self):
        return f"<Product(name='{self.product_name}', expires='{self.expiration_date}')>"