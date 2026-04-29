from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from app.common.configs.settings import settings


def get_async_url(url: str) -> str:
    """Garantit que l'URL utilise un driver async compatible."""
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    if url.startswith("postgres://"):  # format Heroku/Neon raccourci
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    return url

# ── Moteur de connexion ──────────────────────────────
engine = create_async_engine(
    get_async_url(settings.DATABASE_URL),
    echo=settings.DEBUG,      # affiche les requêtes SQL en mode debug
    pool_size=10,              # nombre de connexions simultanées
    max_overflow=20,           # connexions supplémentaires si pool plein
    pool_recycle=300,       # ✅ recycle les connexions toutes les 5 min
    pool_pre_ping=True
)

# ── Fabrique de sessions ─────────────────────────────
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# ── Dépendance globale injectable dans tous les modules ──
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()