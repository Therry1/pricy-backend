from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from app.common.configs.settings import settings

# ── Moteur de connexion ──────────────────────────────
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,      # affiche les requêtes SQL en mode debug
    pool_size=10,              # nombre de connexions simultanées
    max_overflow=20,           # connexions supplémentaires si pool plein
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