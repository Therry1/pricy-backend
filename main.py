import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from contextlib import asynccontextmanager
import httpx
import redis.asyncio as redis
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from app.common.configs.settings import settings
from app.services.service_test.router import router as service_test_router
from dotenv import load_dotenv
load_dotenv(encoding="utf-8")

# ── Variables globales accessibles partout dans l'app ──────────────────────
http_client: httpx.AsyncClient | None = None
redis_client: redis.Redis | None = None
engine = None
SessionLocal = None

@asynccontextmanager
async def lifespan(app: FastAPI):

    # ═══════════════════════════════════════
    #              STARTUP
    # ═══════════════════════════════════════
    global http_client, redis_client, engine, SessionLocal

    # 1. HTTP Client
    http_client = httpx.AsyncClient()
    print("✅ HTTP Client initialisé")

    # 2. Base de données
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print(f"✅ Base de données connectée : {settings.DB_DATABASE}")

    # 3. Redis
    # redis_client = redis.Redis(
    #     host=settings.REDIS_HOST,
    #     port=settings.REDIS_PORT,
    #     password=settings.REDIS_PASSWORD,
    #     decode_responses=True
    # )
    # await redis_client.ping()
    # print(f"✅ Redis connecté : {settings.REDIS_HOST}:{settings.REDIS_PORT}")

    print("⚠️ Redis désactivé")
    
    yield  # ← L'application tourne ici

    # ═══════════════════════════════════════
    #              SHUTDOWN
    # ═══════════════════════════════════════

    # 1. HTTP Client
    await http_client.aclose()
    print("🛑 HTTP Client fermé")

    # 2. Base de données
    engine.dispose()
    print("🛑 Connexion base de données fermée")

    # 3. Redis
    # await redis_client.aclose()
    # print("🛑 Redis fermé")
    print("⚠️ Redis désactivé")


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan
)

app.include_router(service_test_router, prefix='/api/v1')