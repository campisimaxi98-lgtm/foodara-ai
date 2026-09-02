"""
FOODARA AI - Main Application
Punto de entrada de la aplicación FastAPI.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.database.base import Base
from app.database.engine import async_engine
from app.ai import close_ai_service
from app.middleware import RequestIDMiddleware, SecurityHeadersMiddleware
from app.api.routes import (
    health_router,
    auth_router,
    users_router,
    households_router,
    pantry_router,
)
import app.models  # noqa: F401 -- registra todos los modelos en Base.metadata


# Setup logging
setup_logging()
logger = get_logger(__name__)

# Rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.rate_limit_requests}/{settings.rate_limit_window}second"],
    enabled=settings.rate_limit_enabled,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Eventos de ciclo de vida de la aplicación."""
    # Validar seguridad de la configuración antes de arrancar
    settings.validate_security()

    logger.info(f"🚀 {settings.app_name} v{settings.app_version} iniciando...")
    logger.info(f"Environment: {settings.app_env}")
    logger.info(f"Debug: {settings.debug}")

    # Crear tablas solo en entornos de desarrollo/CI.
    # En producción se debe usar Alembic (ver docs/migrations).
    if settings.app_env.lower() not in ("production", "prod"):
        try:
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ Base de datos inicializada (dev)")
        except Exception as e:  # pragma: no cover
            logger.error(f"❌ Error inicializando base de datos: {e}")
    else:
        logger.info("ℹ️ Entorno de producción: se omitió create_all (usar Alembic)")

    yield

    await close_ai_service()
    await async_engine.dispose()
    logger.info(f"👋 {settings.app_name} cerrando...")


# Crear aplicación
app = FastAPI(
    title=settings.app_name,
    description="🍽️ Comprá mejor. Comé mejor. Desperdiciá menos.",
    version=settings.app_version,
    docs_url="/api/docs" if settings.app_env.lower() not in ("production", "prod") else None,
    redoc_url="/api/redoc" if settings.app_env.lower() not in ("production", "prod") else None,
    lifespan=lifespan,
)

# Middleware de seguridad y correlación
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SlowAPIMiddleware)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)


# ============================================
# ROUTERS
# ============================================

# Health & Info
app.include_router(health_router, prefix=settings.api_prefix)

# Authentication
app.include_router(auth_router, prefix=settings.api_prefix)

# Users
app.include_router(users_router, prefix=settings.api_prefix)

# Households (FOODARA HOME)
app.include_router(households_router, prefix=settings.api_prefix)

# Pantry (FOODARA HOME - Despensa digital)
app.include_router(pantry_router, prefix=settings.api_prefix)


# ============================================
# EXCEPTION HANDLERS
# ============================================

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Respuesta cuando se excede el límite de requests."""
    return JSONResponse(
        status_code=429,
        content={"error": "Demasiadas peticiones. Intente más tarde."},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejador global de excepciones."""
    logger.error("Error no manejado", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc) if settings.debug else "Error interno del servidor",
        },
    )


# ============================================
# ROOT ENDPOINT
# ============================================

@app.get("/")
async def root():
    """Endpoint raíz."""
    return {
        "message": "🍽️ FOODARA AI - Comprá mejor. Comé mejor. Desperdiciá menos.",
        "version": settings.app_version,
        "docs": "/api/docs",
        "api_prefix": settings.api_prefix,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
