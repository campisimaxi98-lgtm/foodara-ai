"""
FOODARA AI - Household Routes
Endpoints del módulo FOODARA HOME (hogares).
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.engine import get_async_session
from app.models import User
from app.schemas.household import (
    HouseholdCreate,
    HouseholdUpdate,
    HouseholdResponse,
    HouseholdMemberCreate,
    HouseholdMemberResponse,
)
from app.services.household_service import HouseholdService
from app.api.routes.users import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/households", tags=["households"])


@router.get("/my", response_model=list[HouseholdResponse])
async def list_my_households(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Listar los hogares del usuario actual."""
    service = HouseholdService(session)
    households = await service.list_user_households(current_user.id)
    return households


@router.post("", response_model=HouseholdResponse, status_code=status.HTTP_201_CREATED)
async def create_household(
    data: HouseholdCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Crear un nuevo hogar. El creador queda como owner."""
    service = HouseholdService(session)
    try:
        household = await service.create_household(current_user, data)
        return household
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{household_id}", response_model=HouseholdResponse)
async def get_household(
    household_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Obtener un hogar (solo para miembros)."""
    service = HouseholdService(session)
    household = await service.get_household(household_id)
    if not household:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hogar no encontrado")

    if not await service.is_member(current_user.id, household_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No eres miembro del hogar")

    return household


@router.patch("/{household_id}", response_model=HouseholdResponse)
async def update_household(
    household_id: int,
    data: HouseholdUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Actualizar un hogar (owner/admin)."""
    service = HouseholdService(session)
    household = await service.get_household(household_id)
    if not household:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hogar no encontrado")

    role = await service.get_member_role(current_user.id, household_id)
    if role not in ("owner", "admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso insuficiente")

    try:
        return await service.update_household(household, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{household_id}", status_code=status.HTTP_200_OK)
async def delete_household(
    household_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Eliminar un hogar (solo owner)."""
    service = HouseholdService(session)
    household = await service.get_household(household_id)
    if not household:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hogar no encontrado")

    role = await service.get_member_role(current_user.id, household_id)
    if role != "owner":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el owner puede eliminar el hogar")

    await service.delete_household(household)
    return {"message": "Hogar eliminado"}


@router.post("/{household_id}/members", response_model=HouseholdMemberResponse, status_code=status.HTTP_201_CREATED)
async def add_member(
    household_id: int,
    data: HouseholdMemberCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Agregar un miembro al hogar (owner/admin)."""
    service = HouseholdService(session)
    household = await service.get_household(household_id)
    if not household:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hogar no encontrado")

    role = await service.get_member_role(current_user.id, household_id)
    if role not in ("owner", "admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso insuficiente")

    try:
        member = await service.add_member(
            household_id, data.user_id, role=data.role
        )
        return member
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
