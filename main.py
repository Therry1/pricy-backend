import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from contextlib import asynccontextmanager
import httpx
import redis.asyncio as redis
from fastapi import FastAPI
from app.common.configs.settings import settings
from app.common.configs.database import engine, SessionLocal
from app.services.service_test.router import router as service_test_router
from app.services.stock_manager.router import router as stock_manager_router
from app.services.organization_manager.router import router as organization_manager_router
from app.services.iam_manager.router import router as iam_manager_router



# ── Variables globales ──────────────────────────────────────────────────────
http_client: httpx.AsyncClient | None = None
redis_client: redis.Redis | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global http_client, redis_client

    # ═══════════════════════════════════════
    #              STARTUP
    # ═══════════════════════════════════════

    # 1. HTTP Client
    http_client = httpx.AsyncClient()
    print("✅ HTTP Client initialisé")

    # 2. Base de données
    async with engine.connect() as conn:
        print(f"✅ Base de données connectée : {settings.DB_DATABASE}")

    # 3. Redis (désactivé)
    print("⚠️ Redis désactivé")

    yield

    # ═══════════════════════════════════════
    #              SHUTDOWN
    # ═══════════════════════════════════════

    # 1. HTTP Client
    await http_client.aclose()
    print("🛑 HTTP Client fermé")

    # 2. Base de données
    await engine.dispose()  # ← await obligatoire en async
    print("🛑 Connexion base de données fermée")

    print("⚠️ Redis désactivé")


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan
)

app.include_router(service_test_router, prefix='/api/v1')
app.include_router(stock_manager_router, prefix='/api/v1')
app.include_router(organization_manager_router, prefix='/api/v1')
app.include_router(iam_manager_router, prefix='/api/v1')


