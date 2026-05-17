from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
import bcrypt
from app.common.configs.settings import Settings

# Configuration
settings = Settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES  # Durée de vie du token

# Contexte pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # fonction pour hasher le mot de passe lors de la création d'un nouveau compte
# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# # fonction pour verifier le mot de passe lors de la connexion avec celui hashé en bd
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
    
# fonction pour la création de l'acces token
def create_access_token(data: dict) -> str:
    """Génère le JWT en encapsulant les données fournies."""
    payload = data.copy()
    
    # Définition de l'expiration
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    
    # Encodage du JWT
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt