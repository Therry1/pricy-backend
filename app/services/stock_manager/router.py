"""Router du module stock_manager."""
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.configs.database import get_db

router = APIRouter(prefix="/stock_manager", tags=["stock_manager"])

