"""Handlers du module organization_manager."""

from sqlalchemy import select
from starlette import status
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.models.Organization import Organization
from app.services.organization_manager.schemas import OrganizationCreateSchema, OrganizationListSchema, OrganizationResponseSchema

async def create_organization (data:OrganizationCreateSchema, db : AsyncSession):
    
    data_dict = data.model_dump()

    # convertir les HttpUrl en string
    data_dict["website_url"] = str(data_dict["website_url"]) if data_dict.get("website_url") else None
    data_dict["logo_url"] = str(data_dict["logo_url"]) if data_dict.get("logo_url") else None
    
    # création de l'alias de l'entreprise
    alias_temp = ''
    if len(data_dict['legal_name']) < 6:
        alias_temp = data_dict['legal_name'].ljust(6, 'O')
    else:
        alias_temp  = data_dict['legal_name']
        
    alias_temp = 'pricy_'+ alias_temp
    
    data_dict["alias"] = alias_temp
    
    organization = Organization(**data_dict)
    
    try:
        db.add(organization)
        await db.commit()
        await db.refresh(organization)
    except IntegrityError as exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Conflit d'intégrité : {exception.orig}",
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur inattendue : {str(e)}",
        )
        
    return OrganizationResponseSchema.model_validate(organization)

async def get_organization(db:AsyncSession):
    
    # recupération de toutes les organisations
    organizations_stmt = await db.execute(
        select(
            Organization
        ).where(Organization.deleted_at.is_(None))
    )
    
    organizations = organizations_stmt.scalars().all()
    
    try:
        organization_list_response = {'items' : organizations , 'total': len(organizations)}
        return OrganizationListSchema.model_validate(organization_list_response)
    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur inattendue : {str(exception)}",
        )