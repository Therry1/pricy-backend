"""Handlers du module authentification_manager."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import and_, select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.configs.security import create_access_token, verify_password , hash_password
from app.common.models.UserAccount import UserAccount
from app.services.authentification_manager.schemas import LoginRequest, LoginSuccessResponse, RegisterRequest

async def login( db: AsyncSession ,form_data: LoginRequest):
    
    # 2. Rechercher l'utilisateur dans la table user_accounts
    user_stmt = await db.execute(select(UserAccount).where(
        and_(
            UserAccount.username == form_data.username,
            #UserAccount.hashed_password == hashed_password,
            UserAccount.deleted_at.is_(None)
        )
    ))
    
    user = user_stmt.scalar_one_or_none()
    #raise Exception (f"{str(user.id if user else None)} , {hashed_password}")
    # 2. Vérifier si l'utilisateur existe et si le mot de passe est correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Préparer les données à encapsuler
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "roles": [user.role if user.role else None] # Exemple si tu as des rôles
    }
    
    # 4. Générer le token
    access_token = create_access_token(data=token_data)
    
    # 5. Retourner le token au format standard OAuth2
    login_response = {
        "status_code": status.HTTP_200_OK, 
        "message": "authentification réussie", 
        "error": None, 
        "token" : {
            "access_token": access_token, 
            "refresh_token": None, 
            "token_type": "bearer"
        }
    }
    return LoginSuccessResponse.model_validate(login_response)


async def register (db: AsyncSession , data : RegisterRequest):
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

    # 5. Préparer les données à encapsuler
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "roles":  [user.role if user.role else None] # Exemple si tu as des rôles
    }
    
    # 6. Générer le token
    access_token = create_access_token(data=token_data)
    
    # 7. Retourner le token au format standard OAuth2
    login_response = {
        "status_code": status.HTTP_200_OK, 
        "message": "authentification réussie", 
        "error": None, 
        "token" : {
            "access_token": access_token, 
            "refresh_token": None, 
            "token_type": "bearer"
        }
    }
    
    return LoginSuccessResponse.model_validate(login_response)