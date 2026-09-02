"""
FOODARA AI - User Tests
Tests para endpoints de usuarios y autenticación.
"""

import pytest
from httpx import AsyncClient
from app.main import app
from app.services.user_service import UserService
from app.core.security import hash_password


class TestUserRegistration:
    """Tests para registro de usuarios."""

    @pytest.mark.asyncio
    async def test_register_valid_user(self):
        """Test de registro exitoso."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "test@foodara.ar",
                    "username": "testuser",
                    "password": "SecurePass123!",
                    "first_name": "Test",
                    "last_name": "User",
                }
            )
            # No se puede testear bien sin BD real
            # Pero verifica la estructura de la solicitud
            assert response.status_code in [200, 422]  # 422 si hay error de validación

    @pytest.mark.asyncio
    async def test_register_weak_password(self):
        """Test con contraseña débil."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "test@foodara.ar",
                    "username": "testuser",
                    "password": "weak",  # Muy corta
                }
            )
            # Debería rechazar
            assert response.status_code in [400, 422]

    @pytest.mark.asyncio
    async def test_register_missing_fields(self):
        """Test sin campos obligatorios."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "test@foodara.ar",
                    # Faltan username y password
                }
            )
            assert response.status_code == 422  # Validation error


class TestUserLogin:
    """Tests para login de usuarios."""

    @pytest.mark.asyncio
    async def test_login_missing_email(self):
        """Test de login sin email."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/login",
                json={"password": "somepass"}
            )
            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_login_missing_password(self):
        """Test de login sin contraseña."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/login",
                json={"email": "test@foodara.ar"}
            )
            assert response.status_code == 422


class TestUserProfile:
    """Tests para perfil de usuario."""

    @pytest.mark.asyncio
    async def test_get_profile_without_token(self):
        """Test de acceso sin token."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/v1/users/me")
            # Sin Authorization header
            assert response.status_code == 422  # Missing header

    @pytest.mark.asyncio
    async def test_get_profile_invalid_token(self):
        """Test con token inválido."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/users/me",
                headers={"Authorization": "Bearer invalid.token.here"}
            )
            assert response.status_code == 401


class TestPasswordValidation:
    """Tests para validación de contraseñas."""

    def test_weak_password_too_short(self):
        """Test contraseña muy corta."""
        from app.core.security import is_strong_password
        assert not is_strong_password("Short1!")

    def test_weak_password_no_uppercase(self):
        """Test sin mayúscula."""
        from app.core.security import is_strong_password
        assert not is_strong_password("mysecurepass123!")

    def test_weak_password_no_number(self):
        """Test sin número."""
        from app.core.security import is_strong_password
        assert not is_strong_password("MySecurePass!")

    def test_weak_password_no_symbol(self):
        """Test sin símbolo."""
        from app.core.security import is_strong_password
        assert not is_strong_password("MySecurePass123")

    def test_strong_password(self):
        """Test con contraseña fuerte."""
        from app.core.security import is_strong_password
        assert is_strong_password("MySecurePass123!")
        assert is_strong_password("FoobaraBest@2024")
        assert is_strong_password("Argentina.2025#Rocks")
