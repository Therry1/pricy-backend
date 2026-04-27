"""Schemas Pydantic du module user_manager."""
# schemas/user.py
from pydantic import BaseModel, EmailStr, Field, field_validator, UUID4
from typing import Optional, Any
from datetime import datetime
import re


# ─── Schéma de base (champs communs) ────────────────────────────────────────
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = None
    organization_id: Optional[UUID4] = None
    role: str = Field(default="user")
    preferences: Optional[dict[str, Any]] = None
    language: str = Field(default="fr", max_length=10)
    timezone: str = Field(default="UTC", max_length=50)

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        if v and not re.match(r"^\+?[\d\s\-()]{7,20}$", v):
            raise ValueError("Numéro de téléphone invalide")
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        allowed = {"admin", "manager", "editor", "viewer", "user"}
        if v not in allowed:
            raise ValueError(f"Rôle invalide. Valeurs autorisées : {allowed}")
        return v


# ─── Schéma de création (envoyé par le client) ──────────────────────────────
class UserCreateSchema(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    is_active: bool = True
    is_superuser: bool = False

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Le mot de passe doit contenir au moins une majuscule")
        if not re.search(r"[0-9]", v):
            raise ValueError("Le mot de passe doit contenir au moins un chiffre")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Le mot de passe doit contenir au moins un caractère spécial")
        return v


# ─── Schéma de mise à jour (tous les champs optionnels) ─────────────────────
class UserUpdateSchema(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = None
    role: Optional[str] = None
    preferences: Optional[dict[str, Any]] = None
    language: Optional[str] = Field(None, max_length=10)
    timezone: Optional[str] = Field(None, max_length=50)


# ─── Schéma de réponse (ce qu'on retourne au client) ────────────────────────
class UserResponseSchema(BaseModel):
    id: UUID4
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    avatar_url: Optional[str]
    organization_id: Optional[UUID4]
    role: str
    preferences: Optional[dict[str, Any]]
    language: str
    timezone: str
    is_active: bool
    is_superuser: bool
    last_login: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}  # Permet ORM → Pydantic