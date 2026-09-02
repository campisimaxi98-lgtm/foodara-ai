"""
FOODARA AI - User Routes
Endpoints para gestión completa de usuarios.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.engine import get_async_session
from app.models import User
from app.schemas.user import UserResponse, UserUpdate, UserProfileResponse
from app.schemas.preference import (
    PreferenceResponse,
    PreferenceUpdate,
    FoodaryProfileResponse,
)
from app.services.user_service import UserService, UserPreferenceService
from app.core.security import verify_token_type
import logging


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["users"])


async def get_current_user(
    authorization: str = Header(...),
    session: AsyncSession = Depends(get_async_session)
) -> User:
    """
    Dependency para obtener el usuario actual del token JWT.
    Requerido para todos los endpoints protegidos.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no válido"
        )

    token = authorization.split(" ")[1]
    token_data = verify_token_type(token, "access")

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no válido o expirado"
        )

    result = await session.execute(
        select(User).where(User.id == token_data.user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado"
        )

    return user


# ============================================
# PERFIL DEL USUARIO
# ============================================

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Obtener información del usuario actual.
    """
    logger.info(f"Perfil consultado: {current_user.email}")
    return current_user


@router.get("/me/profile", response_model=FoodaryProfileResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Obtener perfil completo del usuario (datos + preferencias).
    """
    # Obtener preferencias
    pref_service = UserPreferenceService(session)
    preferences = await pref_service.get_preferences(current_user.id)

    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferencias no encontradas"
        )

    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "is_active": current_user.is_active,
        "preferences": preferences
    }


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Actualizar información del usuario actual.
    """
    try:
        user_service = UserService(session)
        updated_user = await user_service.update_user(current_user, user_update)
        return updated_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/me")
async def delete_current_user(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Eliminar cuenta del usuario actual.
    ACCIÓN IRREVERSIBLE.
    """
    user_service = UserService(session)
    await user_service.delete_user(current_user)
    logger.warning(f"Usuario eliminado: {current_user.email}")
    
    return {"message": "Cuenta eliminada"}


@router.post("/me/deactivate")
async def deactivate_current_user(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Desactivar cuenta del usuario (reversible).
    """
    user_service = UserService(session)
    await user_service.deactivate_user(current_user)
    
    return {"message": "Cuenta desactivada"}


@router.post("/me/activate")
async def activate_current_user(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Activar cuenta del usuario.
    """
    if current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La cuenta ya está activa"
        )

    user_service = UserService(session)
    await user_service.activate_user(current_user)
    
    return {"message": "Cuenta activada"}


# ============================================
# PREFERENCIAS
# ============================================

@router.get("/me/preferences", response_model=PreferenceResponse)
async def get_current_user_preferences(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Obtener preferencias del usuario actual.
    """
    pref_service = UserPreferenceService(session)
    preferences = await pref_service.get_preferences(current_user.id)

    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferencias no encontradas"
        )

    return preferences


@router.patch("/me/preferences", response_model=PreferenceResponse)
async def update_current_user_preferences(
    prefs_update: PreferenceUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Actualizar preferencias del usuario actual.
    """
    try:
        pref_service = UserPreferenceService(session)
        
        # Validar preferencias si se actualizan
        if prefs_update.model_dump(exclude_unset=True):
            await pref_service.validate_preferences(prefs_update)
        
        updated_prefs = await pref_service.update_preferences(
            current_user.id,
            prefs_update
        )
        return updated_prefs
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ============================================
# INFORMACIÓN DE OTROS USUARIOS (Admin only)
# ============================================

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener información de un usuario específico.
    Solo administradores o el mismo usuario.
    """
    
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este usuario"
        )

    user_service = UserService(session)
    user = await user_service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return user


@router.get("/{user_id}/preferences", response_model=PreferenceResponse)
async def get_user_preferences(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener preferencias de un usuario específico.
    Solo administradores o el mismo usuario.
    """
    
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso"
        )

    pref_service = UserPreferenceService(session)
    preferences = await pref_service.get_preferences(user_id)

    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferencias no encontradas"
        )

    return preferences
