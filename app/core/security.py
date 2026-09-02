"""
FOODARA AI - Security Module
Manejo de autenticación, hashing y JWT.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
import os

from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import settings


# ============================================
# PASSWORD HASHING
# ============================================

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashear una contraseña usando Argon2.
    NUNCA guardar contraseñas en texto plano.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar una contraseña contra su hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ============================================
# JWT TOKENS
# ============================================


class TokenData(BaseModel):
    """Datos del token JWT"""
    user_id: int
    email: str
    token_type: str


def create_access_token(
    user_id: int,
    email: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Crear un JWT access token.
    Nunca expongas el SECRET_KEY.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode = {
        "user_id": user_id,
        "email": email,
        "token_type": "access",
        "exp": expire
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    return encoded_jwt


def create_refresh_token(
    user_id: int,
    email: str
) -> str:
    """Crear un JWT refresh token."""
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )

    to_encode = {
        "user_id": user_id,
        "email": email,
        "token_type": "refresh",
        "exp": expire
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """Verificar y decodificar un JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        user_id: int = payload.get("user_id")
        email: str = payload.get("email")
        token_type: str = payload.get("token_type")

        if user_id is None or email is None:
            return None

        return TokenData(
            user_id=user_id,
            email=email,
            token_type=token_type
        )
    except JWTError:
        return None


def verify_token_type(token: str, expected_type: str) -> Optional[TokenData]:
    """
    Verificar y decodificar un JWT, forzando que sea del tipo esperado.
    Evita que un access token se use como refresh token y viceversa.
    """
    token_data = verify_token(token)
    if token_data is None:
        return None
    if token_data.token_type != expected_type:
        return None
    return token_data


# ============================================
# VALIDACIONES DE SEGURIDAD
# ============================================


def validate_api_key(api_key: str) -> bool:
    """
    Validar que una API key tenga formato correcto.
    Para validación real, consultar base de datos.
    """
    if not api_key:
        return False
    if len(api_key) < 10:
        return False
    return True


def is_strong_password(password: str) -> bool:
    """Validar que una contraseña sea segura."""
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in "!@#$%^&*" for char in password):
        return False
    return True
