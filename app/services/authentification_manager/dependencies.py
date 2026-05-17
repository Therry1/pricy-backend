"""D�pendances du module authentification_manager."""
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
import uuid
from pydantic import UUID4, ValidationError
from sqlalchemy import and_, select
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.configs.database import get_db
from app.common.configs.settings import Settings
from app.common.models.UserAccount import UserAccount
from app.services.authentification_manager.schemas import TokenPayload

settings = Settings()  

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES  # Durée de vie du token


# Indique à FastAPI où chercher le token (endpoint /token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> UUID4:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Décoder le token avec la clé secrète
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Valider la structure des données récupérées
        token_data = TokenPayload(**payload)
        
        if token_data.sub is None:
            raise credentials_exception
            
    except (jwt.PyJWTError, ValidationError):
        raise credentials_exception
        
    # Optionnel mais recommandé : Aller chercher l'utilisateur frais en BDD
    user_stmt = await db.execute(select(UserAccount).where(
        and_(
            UserAccount.id == token_data.sub,
            UserAccount.deleted_at.is_(None)
        )
    ))
    
    user = user_stmt.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
        
    # Tu peux aussi attacher les données décodées directement si tu veux éviter un appel BDD
    return user.id