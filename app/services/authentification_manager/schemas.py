"""Sch�mas Pydantic du module authentification_manager."""
import re
from typing import Any, Dict, List, Optional

from pydantic import UUID4, BaseModel, EmailStr, Field, field_validator

class TokenPayload (BaseModel):
    sub : UUID4
    username : str
    email : EmailStr
    roles : Optional[List] = None
    
    
class RegisterRequest (BaseModel):
    username: str = Field(..., min_length=5, max_length=50)
    email: EmailStr = Field(..., min_length=9, max_length=50)
    first_name: Optional[str] = Field(..., max_length=100)
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




class LoginRequest(BaseModel):
    username: str
    password: str

class TokenFormat(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str
    
     
class LoginSuccessResponse(BaseModel):
    status_code: int
    message: str
    error : Optional[str] = None
    token : TokenFormat
    
    model_config = {"from_attributes":True}