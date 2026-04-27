"""Router du module user_manager."""
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.configs.database import get_db
from app.services.iam_manager.handler import create_user
from app.services.iam_manager.schemas import UserCreateSchema, UserResponseSchema

router = APIRouter(prefix="/iam_manager", tags=["user_manager"])

@router.post(
    "/register",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouveau compte utilisateur"
)
async def register_user_path(
    payload: UserCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    """
    Crée un nouvel utilisateur avec les informations fournies.

    - **username** : Nom d'utilisateur unique (3-50 caractères)
    - **email** : Adresse email unique et valide
    - **password** : Minimum 8 caractères, 1 majuscule, 1 chiffre, 1 caractère spécial
    """
    return await create_user(db=db, data=payload)