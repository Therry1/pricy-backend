"""Router du module organization_manager."""
from fastapi import APIRouter, Depends
from app.common.configs.database import get_db
from app.services.organization_manager.handler import create_organization
from app.services.organization_manager.schemas import OrganizationCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/organization_manager", tags=["organization_manager"])

@router.post ("/organization", response_model="")
async def create_organization_path (data: OrganizationCreateSchema , db: AsyncSession =  Depends(get_db)):
    return await create_organization(data , db) 



