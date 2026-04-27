"""Schemas Pydantic du module organization_manager."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl


from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime
import uuid


class OrganizationBase(BaseModel):
    legal_name: str = Field(..., max_length=255)
    trade_name: Optional[str] = None
    tax_id: Optional[str] = None
    registration_number: Optional[str] = None
    legal_form: Optional[str] = None
    industry: Optional[str] = None
    founded_date: Optional[datetime] = None

    headquarters_address: Optional[str] = None
    city: Optional[str] = None
    state_province: Optional[str] = None
    zip_code: Optional[str] = None
    country_code: Optional[str] = Field(None, min_length=2, max_length=2)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    website_url: Optional[HttpUrl] = None

    slug: Optional[str] = None
    logo_url: Optional[HttpUrl] = None
    tagline: Optional[str] = None
    description: Optional[str] = None
    primary_color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    social_links: Optional[dict] = None

    status: Optional[str] = "active"
    is_verified: Optional[bool] = False
    size: Optional[str] = None
    default_currency: Optional[str] = Field(default="XAF", min_length=3, max_length=3)
    timezone: Optional[str] = None


    
class OrganizationCreateSchema(OrganizationBase):
    legal_name: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "legal_name": "Entreprise ABC SARL",
                "trade_name": "ABC Store",
                "tax_id": "CM123456789",
                "registration_number": "RC/YAO/2025/B/123",
                "legal_form": "SARL",
                "industry": "Retail",
                "founded_date": "2020-01-01T00:00:00",

                "headquarters_address": "Yaoundé, Cameroun",
                "city": "Yaoundé",
                "state_province": "Centre",
                "zip_code": "0000",
                "country_code": "CM",
                "email": "contact@abc.com",
                "phone_number": "+237600000000",
                "website_url": "https://abc.com",

                "slug": "abc-store",
                "logo_url": "https://abc.com/logo.png",
                "tagline": "Votre boutique de confiance",
                "description": "Entreprise spécialisée dans la vente de produits",
                "primary_color": "#FF5733",
                "social_links": {
                    "facebook": "https://facebook.com/abc",
                    "twitter": "https://twitter.com/abc"
                },

                "status": "active",
                "is_verified": False,
                "size": "11-50 employees",
                "default_currency": "XAF",
                "timezone": "Africa/Douala"
            }
        }
    }
    
class OrganizationUpdateSchema(BaseModel):
    legal_name: Optional[str] = Field(None, max_length=255)
    trade_name: Optional[str] = None
    tax_id: Optional[str] = None
    registration_number: Optional[str] = None
    legal_form: Optional[str] = None
    industry: Optional[str] = None
    founded_date: Optional[datetime] = None

    headquarters_address: Optional[str] = None
    city: Optional[str] = None
    state_province: Optional[str] = None
    zip_code: Optional[str] = None
    country_code: Optional[str] = Field(None, min_length=2, max_length=2)
    email: Optional[str] = None
    phone_number: Optional[str] = None
    website_url: Optional[HttpUrl] = None

    slug: Optional[str] = None
    logo_url: Optional[HttpUrl] = None
    tagline: Optional[str] = None
    description: Optional[str] = None
    primary_color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    social_links: Optional[dict] = None

    status: Optional[str] = None
    is_verified: Optional[bool] = None
    size: Optional[str] = None
    default_currency: Optional[str] = Field(None, min_length=3, max_length=3)
    timezone: Optional[str] = None
    

class OrganizationResponseSchema(OrganizationBase):
    id: uuid.UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    model_config = {"from_attributes": True}
    

class OrganizationListSchema(BaseModel):
    items: List[OrganizationResponseSchema]
    total: int