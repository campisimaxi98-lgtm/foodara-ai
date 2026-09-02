"""
FOODARA AI - Database Engine
Configuración de SQLAlchemy y conexión a PostgreSQL.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine as sync_create_engine
from typing import AsyncGenerator

from app.core.config import settings


# ============================================
# ASYNC ENGINE (para FastAPI)
# ============================================

# Motor asincrónico para la API
async_engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=40,
)

# Session factory asincrónica
async_session_maker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency para inyectar sesión async en endpoints.
    Uso en FastAPI:
        @app.get("/")
        async def endpoint(session: AsyncSession = Depends(get_async_session)):
            ...
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


# ============================================
# SYNC ENGINE (para Alembic)
# ============================================

sync_engine = sync_create_engine(
    settings.database_url_sync,
    echo=settings.debug,
    future=True,
    pool_pre_ping=True,
)


def get_sync_session() -> Session:
    """Obtener sesión sincrónica."""
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(bind=sync_engine, expire_on_commit=False)
    return SessionLocal()
