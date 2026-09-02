"""
FOODARA AI - Health Routes
Endpoints para verificar estado del sistema.

- /health       : liveness - el proceso responde (sin dependencias externas)
- /health/ready : readiness - base de datos y dependencias operativas
- /info         : metadatos del sistema
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.database.engine import get_async_session
from app.ai import get_ai_service

router = APIRouter(prefix="", tags=["health"])


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@router.get("/health")
async def health_check():
    """
    Liveness: el proceso responde.
    Sin dependencias externas para no dar falsos negativos.
    """
    return {
        "status": "healthy",
        "timestamp": _now(),
        "service": settings.app_name,
        "version": settings.app_version,
    }


@router.get("/health/ready")
async def readiness_check(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Readiness: base de datos operativa.
    Usado por orquestadores para decidir si enrutar tráfico.
    """
    db_status = "up"
    try:
        await session.execute(text("SELECT 1"))
    except Exception:
        db_status = "down"

    return {
        "status": "ready" if db_status == "up" else "not_ready",
        "database": db_status,
        "timestamp": _now(),
    }


@router.get("/ai/providers")
async def ai_providers_status():
    """
    Estado de los providers de IA.
    Solo muestra disponibilidad (no expone claves).
    """
    ai_service = await get_ai_service()
    health = await ai_service.health_check()
    available = await ai_service.get_providers_status()

    return {
        "timestamp": _now(),
        "default_provider": settings.default_ai_provider,
        "providers_health": health,
        "providers_available": available,
    }


@router.get("/info")
async def system_info():
    """Información del sistema FOODARA."""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "description": "Comprá mejor. Comé mejor. Desperdiciá menos.",
        "country": settings.country,
        "language": settings.language,
        "currency": settings.currency,
        "timestamp": _now(),
    }
