"""
FOODARA AI - Household Service
Lógica de negocio del módulo FOODARA HOME (hogares).
"""

import logging
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Household, HouseholdMember, User
from app.schemas.household import HouseholdCreate, HouseholdUpdate


logger = logging.getLogger(__name__)


class HouseholdService:
    """Servicio para la gestión de hogares."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_household(
        self,
        owner: User,
        data: HouseholdCreate,
    ) -> Household:
        """Crear un hogar y agregar al propietario como owner."""
        household = Household(
            name=data.name,
            description=data.description,
            budget_ars=data.budget_ars,
            people_count=data.people_count,
        )
        self.session.add(household)
        await self.session.flush()

        member = HouseholdMember(
            household_id=household.id,
            user_id=owner.id,
            role="owner",
        )
        self.session.add(member)
        await self.session.commit()
        await self.session.refresh(household)

        logger.info(f"Hogar creado: {household.name} (owner={owner.username})")
        return household

    async def get_household(self, household_id: int) -> Optional[Household]:
        """Obtener un hogar por ID."""
        result = await self.session.execute(
            select(Household).where(Household.id == household_id)
        )
        return result.scalar_one_or_none()

    async def is_member(self, user_id: int, household_id: int) -> bool:
        """Verificar si un usuario es miembro de un hogar."""
        result = await self.session.execute(
            select(HouseholdMember).where(
                HouseholdMember.household_id == household_id,
                HouseholdMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none() is not None

    async def get_member_role(self, user_id: int, household_id: int) -> Optional[str]:
        """Obtener el rol de un usuario en un hogar."""
        result = await self.session.execute(
            select(HouseholdMember).where(
                HouseholdMember.household_id == household_id,
                HouseholdMember.user_id == user_id,
            )
        )
        member = result.scalar_one_or_none()
        return member.role if member else None

    async def list_user_households(self, user_id: int) -> List[Household]:
        """Listar los hogares del usuario."""
        result = await self.session.execute(
            select(Household)
            .join(HouseholdMember)
            .where(HouseholdMember.user_id == user_id)
            .order_by(Household.created_at)
        )
        return list(result.scalars().all())

    async def add_member(
        self,
        household_id: int,
        user_id: int,
        role: str = "member",
    ) -> HouseholdMember:
        """Agregar un miembro a un hogar."""
        # Evitar duplicados
        if await self.is_member(user_id, household_id):
            raise ValueError("El usuario ya es miembro del hogar")

        member = HouseholdMember(
            household_id=household_id,
            user_id=user_id,
            role=role,
        )
        self.session.add(member)
        await self.session.commit()
        await self.session.refresh(member)

        logger.info(f"Miembro {user_id} agregado al hogar {household_id}")
        return member

    async def update_household(
        self,
        household: Household,
        data: HouseholdUpdate,
    ) -> Household:
        """Actualizar un hogar."""
        allowed = {
            "name", "description", "budget_ars", "people_count", "is_active",
        }
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field in allowed:
                setattr(household, field, value)

        self.session.add(household)
        await self.session.commit()
        await self.session.refresh(household)

        logger.info(f"Hogar actualizado: {household.name}")
        return household

    async def delete_household(self, household: Household) -> None:
        """Eliminar un hogar (hard delete)."""
        await self.session.delete(household)
        await self.session.commit()
        logger.info(f"Hogar eliminado: {household.name}")
