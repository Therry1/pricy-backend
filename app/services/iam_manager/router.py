"""Router du module iam_manager."""
from fastapi import APIRouter, Depends, Query
from uuid import UUID
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.configs.database import get_db
from app.services.authentification_manager.dependencies import get_current_user
from app.services.iam_manager.handler import config_role, create_role
from app.services.iam_manager.schemas import RoleConfigSchema, RoleCreateSchema, RoleResponseSchema

router = APIRouter(prefix="/iam_manager", tags=["iam_manager"])

@router.post('/role', response_model=RoleResponseSchema)
async def create_role_path(payload: RoleCreateSchema , db : AsyncSession = Depends(get_db)):
    return await create_role (db , payload)

@router.get('/roles')
async def create_role_path(user_account_id = Depends(get_current_user)):
    return user_account_id if user_account_id else "je suis la"

@router.post('role/config' , response_model=RoleResponseSchema)
async def config_role_path(payload : RoleConfigSchema , db : AsyncSession = Depends(get_db), user_account_id = Depends(get_current_user)):
    return await config_role (db , payload)
