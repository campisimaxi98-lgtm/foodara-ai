#!/bin/sh
# FOODARA AI - Startup script for production (Docker/Render)
# Asegura que las tablas existan y arranca uvicorn.

set -e

echo "🚀 FOODARA AI - Starting production server..."

# Uso una variable temporal para no modificar el repositorio.
# En producción, creamos las tablas si no existen (sin migraciones iniciales).
# Cuando existan migraciones Alembic, reemplazar por: alembic upgrade head
if [ "${AUTO_CREATE_TABLES:-true}" = "true" ]; then
  echo "🗄️  Ensuring database tables exist..."
  python -c "
import asyncio
from app.database.engine import async_engine
from app.database.base import Base
import app.models  # noqa: F401

async def init():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init())
print('✅ Database tables ready')
"
fi

echo "📡 Starting uvicorn on :8000"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
