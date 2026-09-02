"""
FOODARA AI - API Routes
Importa todos los routers de la API.
"""

from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.households import router as households_router
from app.api.routes.pantry import router as pantry_router

__all__ = [
    "health_router",
    "auth_router",
    "users_router",
    "households_router",
    "pantry_router",
]
