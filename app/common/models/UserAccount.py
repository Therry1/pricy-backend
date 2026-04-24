from datetime import datetime
import uuid

from sqlalchemy import CHAR, JSON, UUID, Column, Float, ForeignKey, Integer, String, Boolean, DateTime, Text, func
from app.common.models.base import Base

class UserAccount(Base):
    __tablename__ = "user_accounts"

    # 1. Primary Identifiers
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    
    # 2. Security & Authentication
    # Stockez TOUJOURS le hash du mot de passe, jamais le texte brut !
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, server_default="true")
    is_superuser = Column(Boolean, default=False, server_default="false")
    
    # 3. Personal Information
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone_number = Column(String(20))
    avatar_url = Column(Text) # Lien vers la photo de profil
    
    # 4. Role & Organization
    # Un utilisateur appartient généralement à une organisation
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    role = Column(String(50), default="user") # ex: 'admin', 'manager', 'editor', 'viewer'
    
    # 5. Preferences & Localization
    preferences = Column(JSON) # ex: {"theme": "dark", "notifications": true}
    language = Column(String(10), default="fr")
    timezone = Column(String(50), default="UTC")

    # 6. Audit & Tracking
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', role='{self.role}')>"