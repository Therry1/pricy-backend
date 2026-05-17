"""Router du module authentification_manager."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.configs.database import get_db
from app.services.authentification_manager.handler import login, register
from app.services.authentification_manager.schemas import LoginRequest, RegisterRequest

router = APIRouter(prefix="/authentification_manager", tags=["authentification_manager"])

@router.post('/register')
async def register_path (payload :RegisterRequest , db : AsyncSession = Depends(get_db)):
    return await register(db , payload)

@router.post('/login')
async def login_path (payload :LoginRequest , db : AsyncSession = Depends(get_db)):
    return await login(db , payload)


