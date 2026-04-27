"""Handlers du module organization_manager."""

from starlette import status
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.models.Organization import Organization
from app.services.organization_manager.schemas import OrganizationCreateSchema, OrganizationResponseSchema

async def create_organization (data:OrganizationCreateSchema, db : AsyncSession):
    data_dict = data.model_dump()

    # convertir les HttpUrl en string
    data_dict["website_url"] = str(data_dict["website_url"]) if data_dict.get("website_url") else None
    data_dict["logo_url"] = str(data_dict["logo_url"]) if data_dict.get("logo_url") else None

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