"""
FOODARA AI - Authentication Routes
Endpoints para autenticación y autorización.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.database.engine import get_async_session
from app.models import User
from app.schemas.user import (
    UserCreate,
    TokenRequest,
    TokenResponse,
    UserResponse,
    RefreshRequest,
    AccessTokenResponse,
)
from app.schemas.preference import PreferenceCreate, FoodaryProfileCreate
from app.services.user_service import UserService
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token_type,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Registrar un nuevo usuario FOODARA.
    
    Crea el usuario y sus preferencias por defecto.
    """
    
    try:
        user_service = UserService(session)
        
        # Crear usuario con preferencias por defecto
        user = await user_service.create_user(user_data)
        
        logger.info(f"Usuario registrado: {user.email}")
        
        # Generar tokens
        access_token = create_access_token(user.id, user.email)
        refresh_token = create_refresh_token(user.id, user.email)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en registro: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar usuario"
        )


@router.post("/register-full", response_model=TokenResponse)
async def register_with_preferences(
    profile_data: FoodaryProfileCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Registrar un nuevo usuario con preferencias personalizadas.
    
    Permite configurar preferencias durante el registro.
    """
    
    try:
        user_service = UserService(session)
        
        # Crear usuario con preferencias personalizadas
        user_create = UserCreate(
            email=profile_data.email,
            username=profile_data.username,
            password=profile_data.password,
            first_name=profile_data.first_name,
            last_name=profile_data.last_name,
        )
        
        user = await user_service.create_user(
            user_create,
            preferences=profile_data.preferences
        )
        
        logger.info(f"Usuario registrado con preferencias: {user.email}")
        
        # Generar tokens
        access_token = create_access_token(user.id, user.email)
        refresh_token = create_refresh_token(user.id, user.email)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en registro completo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar usuario"
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: TokenRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Login de usuario FOODARA.
    
    Verifica credenciales y retorna tokens JWT.
    """
    
    try:
        user_service = UserService(session)
        
        # Buscar usuario por email
        user = await user_service.get_user_by_email(credentials.email)

        if not user:
            logger.warning(f"Intento de login con email no registrado: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )

        # Verificar contraseña
        if not verify_password(credentials.password, user.hashed_password):
            logger.warning(f"Intento de login con contraseña incorrecta: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )

        if not user.is_active:
            logger.warning(f"Intento de login con usuario desactivado: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario desactivado"
            )

        # Generar tokens
        access_token = create_access_token(user.id, user.email)
        refresh_token = create_refresh_token(user.id, user.email)

        logger.info(f"Login exitoso: {user.email}")

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error en autenticación"
        )


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(
    body: RefreshRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Renovar el access token usando un refresh token válido.

    El refresh token debe ser de tipo "refresh" (lo verifica el servidor).
    Devuelve un nuevo access token y un nuevo refresh token (rotación).
    """
    try:
        token_data = verify_token_type(body.refresh_token, "refresh")
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token no válido o expirado"
            )

        user_service = UserService(session)
        user = await user_service.get_user_by_id(token_data.user_id)

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

        new_access = create_access_token(user.id, user.email)
        new_refresh = create_refresh_token(user.id, user.email)

        return AccessTokenResponse(
            access_token=new_access,
            refresh_token=new_refresh,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en refresh: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al renovar token"
        )
