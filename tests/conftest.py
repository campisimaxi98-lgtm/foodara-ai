"""
FOODARA AI - Test Configuration
Fixtures y configuración para testing.
"""

import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient

from app.main import app
from app.database.base import Base
from app.core.config import settings


# ============================================
# DATABASE FIXTURES
# ============================================

@pytest.fixture(scope="session")
def event_loop():
    """Crear event loop para toda la sesión de tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db():
    """
    Fixture de base de datos para tests.
    Crea una BD en memoria para cada test.
    """
    # Usar SQLite en memoria para tests
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with SessionLocal() as session:
        yield session

    await engine.dispose()


# ============================================
# CLIENT FIXTURES
# ============================================

@pytest.fixture
async def test_client():
    """
    Cliente HTTP para testing.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# ============================================
# SAMPLE DATA
# ============================================

@pytest.fixture
def sample_user_data():
    """Datos de usuario de ejemplo."""
    return {
        "email": "test@foodara.ar",
        "username": "testuser",
        "password": "SecurePass123!",
        "first_name": "Test",
        "last_name": "User",
    }


@pytest.fixture
def sample_preferences_data():
    """Datos de preferencias de ejemplo."""
    return {
        "currency": "ARS",
        "language": "es",
        "timezone": "America/Argentina/Buenos_Aires",
        "preferred_budget_ars": 75000,
        "people_at_home": 4,
        "cooking_time_available_minutes": 45,
        "vegetarian": False,
        "vegan": False,
        "gluten_free": False,
        "dairy_free": False,
    }


@pytest.fixture
def invalid_password():
    """Contraseña inválida para testing."""
    return "weak"


@pytest.fixture
def strong_passwords():
    """Contraseñas válidas para testing."""
    return [
        "SecurePass123!",
        "FoobaraBest@2024",
        "Argentina.2025#Rocks",
        "MyApp$PW98",
    ]


# ============================================
# PYTEST MARKERS
# ============================================

def pytest_configure(config):
    """Registrar markers personalizados."""
    config.addinivalue_line(
        "markers", "asyncio: marca test como asincrónico"
    )
    config.addinivalue_line(
        "markers", "unit: test unitario"
    )
    config.addinivalue_line(
        "markers", "integration: test de integración"
    )
