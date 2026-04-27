"""Schemas Pydantic du module stock_manager."""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, condecimal


# ─────────────────────────────────────────
#        SCHEMAS DE BASE
# ─────────────────────────────────────────

class NutritionFacts(BaseModel):
    """Schéma pour les informations nutritionnelles"""
    calories: Optional[float] = None
    proteins: Optional[float] = None
    carbohydrates: Optional[float] = None
    fats: Optional[float] = None
    fiber: Optional[float] = None
    sodium: Optional[float] = None


# ─────────────────────────────────────────
#        SCHEMAS REQUETES (entrée)
# ─────────────────────────────────────────

class ProductCreateSchema(BaseModel):
    """Données nécessaires pour créer un produit"""
    product_name: str = Field(..., min_length=2, max_length=255)

    # Spécificités alimentaires
    allergens: Optional[list[str]] = Field(default_factory=list)
    nutrition_facts: Optional[NutritionFacts] = None

    # Dates critiques
    expiration_date: Optional[datetime] = None
    supply_threshold: int = Field(..., gt=0)
    critical_threshold: int = Field(..., gt=0)

    # Conservation & Physique
    weight_unit: Optional[str] = Field(default="kg", max_length=10)
    storage_instructions: Optional[str] = Field(None, max_length=255)

    # Commercial
    unit_price: float = Field(..., gt=0)
    status: Optional[str] = Field(default="available")

    # Relations
    organization_id: uuid.UUID
    packaging_id: Optional[uuid.UUID] = None

    class Config:
        json_schema_extra = {
            "example": {
                "product_name": "Lait entier",
                "allergens": ["milk"],
                "nutrition_facts": {
                    "calories": 61,
                    "proteins": 3.2,
                    "fats": 3.5
                },
                "expiration_date": "2025-12-31T00:00:00",
                "supply_threshold": 100,
                "critical_threshold": 20,
                "weight_unit": "L",
                "storage_instructions": "Keep refrigerated",
                "unit_price": 1.5,
                "status": "available",
                "organization_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class ProductUpdateSchema(BaseModel):
    """Toutes les données sont optionnelles pour la mise à jour"""
    product_name: Optional[str] = Field(None, min_length=2, max_length=255)
    allergens: Optional[list[str]] = None
    nutrition_facts: Optional[NutritionFacts] = None
    expiration_date: Optional[datetime] = None
    supply_threshold: Optional[int] = Field(None, gt=0)
    critical_threshold: Optional[int] = Field(None, gt=0)
    weight_unit: Optional[str] = Field(None, max_length=10)
    storage_instructions: Optional[str] = Field(None, max_length=255)
    unit_price: Optional[float] = Field(None, gt=0)
    status: Optional[str] = None
    packaging_id: Optional[uuid.UUID] = None


# ─────────────────────────────────────────
#        SCHEMAS REPONSES (sortie)
# ─────────────────────────────────────────

class ProductResponseSchema(BaseModel):
    """Données retournées au client"""
    id: uuid.UUID
    product_name: str
    allergens: Optional[list[str]] = None
    nutrition_facts: Optional[NutritionFacts] = None
    expiration_date: Optional[datetime] = None
    supply_threshold: int
    critical_threshold: int
    weight_unit: Optional[str] = None
    storage_instructions: Optional[str] = None
    unit_price: float
    status: str
    state: int
    organization_id: uuid.UUID
    packaging_id: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}  # permet la conversion depuis un objet SQLAlchemy