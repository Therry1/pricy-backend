from pathlib import Path
from typing import Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

ENV_FILE = Path(__file__).resolve().parents[3] / ".env"

class Settings(BaseSettings):
    APP_NAME: str = None
    DEBUG: bool = False
    DB_CONNECTION: str = "postgresql"
    DB_HOST: str
    DB_PORT: int = 5432
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None

    DATABASE_URL: Optional[str] = None  # ✅ Plus de doublon, None par défaut

    model_config = {"env_file": str(ENV_FILE), "env_file_encoding": "utf-8", "extra": "ignore"}

    @model_validator(mode="after")
    def build_database_url(self) -> "Settings":
        # ✅ On construit l'URL seulement si elle n'est pas déjà définie
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"{self.DB_CONNECTION}://"
                f"{self.DB_USERNAME}:{quote_plus(self.DB_PASSWORD)}"
                f"@{self.DB_HOST}:{self.DB_PORT}"
                f"/{self.DB_DATABASE}"
            )
        return self

settings = Settings()