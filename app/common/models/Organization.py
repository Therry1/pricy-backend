
from datetime import datetime
import uuid

from sqlalchemy import CHAR, JSON, UUID, Column, Integer, String, Boolean, DateTime, Text, func
from app.common.models.base import Base

class Organization(Base):
    __tablename__ = "organizations"

    # 1. Identity & Legal Info
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    legal_name = Column(String(255), nullable=False)
    trade_name = Column(String(255))
    tax_id = Column(String(100), unique=True, index=True)
    registration_number = Column(String(100), unique=True)
    legal_form = Column(String(50))  # ex: SARL, SA, LLC
    industry = Column(String(100))
    founded_date = Column(DateTime)

    # 2. Contact & Location
    headquarters_address = Column(Text)
    city = Column(String(100))
    state_province = Column(String(100))
    zip_code = Column(String(20))
    country_code = Column(CHAR(2), index=True)  # ex: 'CM', 'FR'
    email = Column(String(150), index=True)
    phone_number = Column(String(50))
    website_url = Column(Text)

    # 3. Branding & UI
    slug = Column(String(255), unique=True, index=True)
    logo_url = Column(Text)
    tagline = Column(String(255))
    description = Column(Text)
    primary_color = Column(CHAR(7))  # format Hex: #FFFFFF
    social_links = Column(JSON)  # Pour stocker {'linkedin': '...', 'twitter': '...'}

    # 4. System & Status
    status = Column(String(20), default="active", server_default="active")
    is_verified = Column(Boolean, default=False, server_default="false")
    size = Column(String(50))  # ex: '11-50 employees'
    default_currency = Column(CHAR(3), default="XAF")
    timezone = Column(String(50))

    # 5. Audit Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Organization(name='{self.trade_name or self.legal_name}', status='{self.status}')>"