"""Handlers du module user_manager."""
# services/user_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.common.models.UserAccount import UserAccount
from app.services.iam_manager.helper import hash_password
from app.services.iam_manager.schemas import UserCreateSchema, UserResponseSchema



async def create_user(db: AsyncSession, data: UserCreateSchema) -> UserResponseSchema:

    # 1. Vérifier unicité email
    result = await db.execute(select(UserAccount).where(UserAccount.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un compte avec cet email existe déjà"
        )

    # 2. Vérifier unicité username
    result = await db.execute(select(UserAccount).where(UserAccount.username == data.username))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce nom d'utilisateur est déjà pris"
        )

    # 3. Préparer les données (exclure password brut, ajouter le hash)
    user_data = data.model_dump(exclude={"password"})
    user_data["hashed_password"] = hash_password(data.password)

    # 4. Créer l'instance et persister
    user = UserAccount(**user_data)
    db.add(user)

    try:
        await db.commit()
        await db.refresh(user)  # Récupère les valeurs générées par le serveur (id, created_at...)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du compte : {str(e)}"
        )

    return UserResponseSchema.model_validate(user)