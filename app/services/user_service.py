"""
FOODARA AI - User Service
Servicio que centraliza lógica de negocio de usuarios.
"""

import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User, UserPreference
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.preference import PreferenceCreate, PreferenceUpdate
from app.core.security import hash_password, is_strong_password


logger = logging.getLogger(__name__)


class UserService:
    """Servicio para gestión de usuarios."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(
        self,
        user_data: UserCreate,
        preferences: Optional[PreferenceCreate] = None
    ) -> User:
        """
        Crear un nuevo usuario con preferencias.
        
        Args:
            user_data: Datos del usuario
            preferences: Preferencias del usuario
            
        Returns:
            Usuario creado
            
        Raises:
            ValueError: Si hay error en validación
        """
        
        # Validar contraseña
        if not is_strong_password(user_data.password):
            raise ValueError(
                "La contraseña debe tener al menos 8 caracteres, "
                "mayúscula, número y símbolo especial"
            )

        # Verificar que el email no exista
        result = await self.session.execute(
            select(User).where(User.email == user_data.email)
        )
        if result.scalar_one_or_none():
            raise ValueError("El email ya está registrado")

        # Verificar que el username no exista
        result = await self.session.execute(
            select(User).where(User.username == user_data.username)
        )
        if result.scalar_one_or_none():
            raise ValueError("El usuario ya existe")

        # Crear usuario
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )
        self.session.add(user)
        await self.session.flush()

        # Validar preferencias si se proporcionan
        if preferences:
            pref_service = UserPreferenceService(self.session)
            await pref_service.validate_preferences(preferences)

            user_prefs = UserPreference(
                user_id=user.id,
                currency=preferences.currency,
                language=preferences.language,
                timezone=preferences.timezone,
                preferred_budget_ars=preferences.preferred_budget_ars,
                people_at_home=preferences.people_at_home,
                cooking_time_available_minutes=preferences.cooking_time_available_minutes,
                vegetarian=preferences.vegetarian,
                vegan=preferences.vegan,
                gluten_free=preferences.gluten_free,
                dairy_free=preferences.dairy_free,
                email_notifications=preferences.email_notifications,
                waste_alerts=preferences.waste_alerts,
                budget_alerts=preferences.budget_alerts,
            )
        else:
            # Preferencias por defecto
            user_prefs = UserPreference(user_id=user.id)

        self.session.add(user_prefs)
        await self.session.commit()
        await self.session.refresh(user)

        logger.info(f"Usuario creado: {user.username}")
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Obtener usuario por ID."""
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email."""
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Obtener usuario por username."""
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def update_user(
        self,
        user: User,
        user_update: UserUpdate
    ) -> User:
        """Actualizar datos del usuario."""
        
        if user_update.first_name is not None:
            user.first_name = user_update.first_name
        
        if user_update.last_name is not None:
            user.last_name = user_update.last_name

        if user_update.email is not None:
            # Verificar que el nuevo email no exista
            result = await self.session.execute(
                select(User).where(
                    User.email == user_update.email,
                    User.id != user.id
                )
            )
            if result.scalar_one_or_none():
                raise ValueError("El email ya está en uso")
            user.email = user_update.email

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        logger.info(f"Usuario actualizado: {user.email}")
        return user

    async def delete_user(self, user: User) -> None:
        """Eliminar usuario."""
        await self.session.delete(user)
        await self.session.commit()
        logger.info(f"Usuario eliminado: {user.email}")

    async def deactivate_user(self, user: User) -> User:
        """Desactivar usuario."""
        user.is_active = False
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        logger.warning(f"Usuario desactivado: {user.email}")
        return user

    async def activate_user(self, user: User) -> User:
        """Activar usuario."""
        user.is_active = True
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        logger.info(f"Usuario activado: {user.email}")
        return user


class UserPreferenceService:
    """Servicio para gestión de preferencias."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_preferences(self, user_id: int) -> Optional[UserPreference]:
        """Obtener preferencias del usuario."""
        result = await self.session.execute(
            select(UserPreference).where(UserPreference.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def update_preferences(
        self,
        user_id: int,
        prefs_update: PreferenceUpdate
    ) -> UserPreference:
        """Actualizar preferencias del usuario."""
        
        # Obtener preferencias existentes
        prefs = await self.get_preferences(user_id)
        if not prefs:
            raise ValueError("Preferencias no encontradas")

        # Actualizar solo los campos permitidos y presentes
        allowed_fields = {
            "currency", "language", "timezone", "preferred_budget_ars",
            "people_at_home", "cooking_time_available_minutes",
            "vegetarian", "vegan", "gluten_free", "dairy_free",
            "email_notifications", "waste_alerts", "budget_alerts",
        }
        update_data = prefs_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field in allowed_fields:
                setattr(prefs, field, value)

        self.session.add(prefs)
        await self.session.commit()
        await self.session.refresh(prefs)

        logger.info(f"Preferencias actualizadas para usuario: {user_id}")
        return prefs

    async def validate_preferences(
        self,
        preferences,
    ) -> bool:
        """Validar preferencias. Acepta PreferenceCreate o PreferenceUpdate."""
        
        # Validar presupuesto
        budget = getattr(preferences, "preferred_budget_ars", None)
        if budget is not None and budget < 0:
            raise ValueError("El presupuesto no puede ser negativo")

        # Validar cantidad de personas
        people = getattr(preferences, "people_at_home", None)
        if people is not None and (people < 1 or people > 20):
            raise ValueError("La cantidad de personas debe estar entre 1 y 20")

        # Validar tiempo de cocina
        cooking = getattr(preferences, "cooking_time_available_minutes", None)
        if cooking is not None and (cooking < 5 or cooking > 480):
            raise ValueError("El tiempo debe estar entre 5 y 480 minutos")

        return True
