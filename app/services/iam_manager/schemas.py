"""Sch�mas Pydantic du module iam_manager."""
from pydantic import BaseModel, EmailStr, Field, field_validator, UUID4
from typing import List, Optional, Any
from datetime import datetime
import re

    
# Schema pour la gestion des roles
class RoleCreateSchema (BaseModel):
    label : str
    code : str
    description : str
    permissions_associate : Optional[List[UUID4]] = None

class PermissionCreateSchema (BaseModel):
    label : str
    code : str
    description : str
    permissions_associate : Optional[List[UUID4]] = None

class PermissionResponseSchema (BaseModel):
    id : UUID4
    label : str
    code : str
    description : str
    created_at : Optional[datetime] = None
    updated_at : Optional[datetime] = None
    
    model_config = {'from_attributes': True}
    
class RoleResponseSchema (BaseModel):
    id : UUID4
    label : str
    code : str
    description : str
    created_at : Optional[datetime] = None
    updated_at : Optional[datetime] = None
    permissions_associate : Optional[List[PermissionResponseSchema]] = None
    
    model_config = {'from_attributes': True}
    
class RoleConfigSchema (BaseModel):
    role_id : UUID4
    permissions_associate: List[UUID4]
    