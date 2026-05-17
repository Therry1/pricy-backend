"""Schemas Pydantic du module product_manager."""
import uuid
from datetime import datetime
from typing import Dict, List, Optional
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
    unit_measure: str = Field(...)
    weight_unit: Optional[str] = Field(default="kg", max_length=10)
    storage_instructions: Optional[str] = Field(None, max_length=255)

    # Commercial
    purchase_unit_price: float = Field(..., gt=0)
    salling_unit_price: float = Field(None, gt=0)
    
    status: Optional[str] = Field(default="available")

    # Relations
    organization_id: uuid.UUID
    packagings_id: Dict[uuid.UUID, int] = Field(
        default_factory=dict, 
        description="Mapping entre l'ID du packaging et le ratio de conversion"
    )

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
                "unit_measure": "Kg",
                "weight_unit": "L",
                "storage_instructions": "Keep refrigerated",
                "purchase_unit_price": 10000,
                "salling_unit_price": 20000,
                "status": "available",
                "packagings_id": {
                    "550e8400-e29b-41d4-a716-446655440000": 50,
                    "67890123-e29b-41d4-a716-446655441111": 25
                },
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
    purchase_unit_price: Optional[float] = Field(None, gt=0)
    salling_unit_price: Optional[float] = Field(None, gt=0)
    status: Optional[str] = None
    packagings_id: Optional[Dict[uuid.UUID , int]] = None


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
    purchase_unit_price: float
    salling_unit_price: Optional[float]
    is_kit : bool
    is_sallable : bool
    status: str
    state: int
    organization_id: uuid.UUID
    packagings_id: Dict[uuid.UUID , int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}  # permet la conversion depuis un objet SQLAlchemy
    
class ListProductResponseSchema(BaseModel):
    status_code: int
    items : List[ProductResponseSchema]
    
    
# ────────────────────────────────────────────────────
#        SCHEMAS DE CONSTITUTION D'UN PODUIT (sortie)
# ────────────────────────────────────────────────────

class ProductForConstitution(BaseModel):
    component_id : uuid.UUID = Field(...)
    quantity : float = Field(...)
    unit : str = Field(...)
    
    
    
class ConstituateProductSchema(BaseModel):
    components: List[ProductForConstitution]
    product_name: str
    # Dates critiques
    expiration_date: Optional[datetime] = None
    supply_threshold: int = Field(..., gt=0)
    critical_threshold: int = Field(..., gt=0)

    # Conservation & Physique
    unit_measure: str = Field(...)
    weight_unit: Optional[str] = Field(default="kg", max_length=10)
    storage_instructions: Optional[str] = Field(None, max_length=255)

    # Commercial
    purchase_unit_price: float = Field(..., gt=0)
    salling_unit_price: float = Field(None, gt=0)
    
    status: Optional[str] = Field(default="available")

    # Relations
    organization_id: uuid.UUID
    packagings_id: Dict[uuid.UUID, int] = Field(
        default_factory=dict, 
        description="Mapping entre l'ID du packaging et le ratio de conversion"
    )