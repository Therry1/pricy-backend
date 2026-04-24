from sqlalchemy import UUID, Column, DateTime, Integer, Float, ForeignKey, String, func

from app.common.models.base import Base


class ProductCatalogue(Base):
    __tablename__ = "product_catalogues"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    component_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    
    # Audit
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))