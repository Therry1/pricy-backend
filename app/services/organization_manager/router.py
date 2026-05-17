"""Router du module organization_manager."""
from fastapi import APIRouter, Depends
from app.common.configs.database import get_db
from app.services.organization_manager.handler import create_organization, get_organization
from app.services.organization_manager.schemas import OrganizationCreateSchema, OrganizationListSchema
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/organization_manager", tags=["organization_manager"])

@router.post ("/organization", response_model="")
async def create_organization_path (data: OrganizationCreateSchema , db: AsyncSession =  Depends(get_db)):
    return await create_organization(data , db) 

@router.get ('/organization', response_model=OrganizationListSchema)
async def get_organizations_path(db:AsyncSession = Depends(get_db)):
    return await get_organization(db)



