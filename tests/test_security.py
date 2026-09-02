"""
FOODARA AI - Security Tests
Tests para funciones de seguridad.
"""

import pytest
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token,
    is_strong_password,
)


def test_password_hashing():
    """Test de hashing de contraseñas."""
    password = "MySecure123!Pass"
    hashed = hash_password(password)
    
    # El hash no debe ser igual al password original
    assert hashed != password
    
    # Debe poder verificar la contraseña
    assert verify_password(password, hashed)
    
    # No debe verificar contraseñas incorrectas
    assert not verify_password("WrongPassword", hashed)


def test_strong_password_validation():
    """Test de validación de contraseñas fuertes."""
    # Contraseña válida
    assert is_strong_password("MySecure123!Pass")
    
    # Muy corta
    assert not is_strong_password("Short1!")
    
    # Sin mayúscula
    assert not is_strong_password("mysecure123!pass")
    
    # Sin número
    assert not is_strong_password("MySecurePass!")
    
    # Sin símbolo
    assert not is_strong_password("MySecure123Pass")


def test_jwt_token_creation():
    """Test de creación de JWT."""
    user_id = 1
    email = "test@foodara.ar"
    
    token = create_access_token(user_id, email)
    
    assert isinstance(token, str)
    assert len(token) > 0


def test_jwt_token_verification():
    """Test de verificación de JWT."""
    user_id = 1
    email = "test@foodara.ar"
    
    token = create_access_token(user_id, email)
    token_data = verify_token(token)
    
    assert token_data is not None
    assert token_data.user_id == user_id
    assert token_data.email == email
    assert token_data.token_type == "access"


def test_invalid_token_verification():
    """Test de verificación de token inválido."""
    invalid_token = "invalid.token.here"
    token_data = verify_token(invalid_token)
    
    assert token_data is None
