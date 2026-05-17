"""Handlers du module iam_manager."""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from fastapi import HTTPException, status

from app.common.models.Role import Role
from app.common.models.RolePermission import RolePermission
from app.services.iam_manager.schemas import RoleConfigSchema, RoleCreateSchema, RoleResponseSchema


async def create_role (db : AsyncSession , payload : RoleCreateSchema):
    data = payload.model_dump(exclude={'permissions_associate'})
    try:
        role = Role(**data)
        db.add(role)
        await db.flush()
    except Exception as Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"an error occurent on creation of role. Exception : {str(exception)}"  
        )
    
    if len(payload.permissions_associate) > 0:
        role_permission_data = [
            {
                'role_id' : role.id,
                'permission_id' : permission_id
            } for permission_id in payload.permissions_associate
        ]
        
        try:
            query = insert(RolePermission).values(role_permission_data)
            query_result = await db.execute(query)
            db.add(query_result)
            await db.commit()
            
            return RoleResponseSchema.model_validate(role)
        except Exception as exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"an error occurent on affectation of permissions to role. Exception : {str(exception)}"  
            )
    else:
        return RoleResponseSchema.model_validate(role)

async def config_role (db : AsyncSession , payload : RoleConfigSchema):
    # normalisation des données à stocker
    role_permission_data = [
        {
            'role_id' : payload.role_id,
            'permission_id' : permission_id
        } for permission_id in payload.permissions_associate
    ]
    
    try:
        #requete d'insertion de la configuration du role
        query = insert(RolePermission).values(role_permission_data)
    except Exception as exception:
        return 'ok'
    
    return 'ok'
