"""
FOODARA AI - Pantry Routes
Endpoints de la despensa digital (FOODARA HOME).
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.engine import get_async_session
from app.models import User
from app.schemas.pantry import (
    PantryItemCreate,
    PantryItemUpdate,
    PantryItemResponse,
    PantrySummary,
)
from app.services.pantry_service import PantryService
from app.api.routes.users import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/pantry", tags=["pantry"])


@router.post("/items", response_model=PantryItemResponse, status_code=status.HTTP_201_CREATED)
async def add_pantry_item(
    data: PantryItemCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Agregar un alimento a la despensa del usuario."""
    service = PantryService(session)
    try:
        item = await service.add_item(current_user, data)
        return item
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/items", response_model=list[PantryItemResponse])
async def list_pantry_items(
    status_filter: str = Query(default=None, alias="status"),
    location: str = Query(default=None),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Listar los items de la despensa del usuario."""
    service = PantryService(session)
    return await service.list_items(current_user.id, status=status_filter, location=location)


@router.get("/summary", response_model=PantrySummary)
async def pantry_summary(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Resumen determinístico de la despensa."""
    service = PantryService(session)
    return await service.get_summary(current_user.id)


@router.get("/expiring", response_model=list[PantryItemResponse])
async def expiring_items(
    days: int = Query(default=7, ge=0, le=365),
    include_expired: bool = Query(default=False),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Items próximos a vencer. Avisa: 'El yogur vence en 2 días'."""
    service = PantryService(session)
    return await service.expiring_items(
        current_user.id, days=days, include_expired=include_expired
    )


@router.get("/expired", response_model=list[PantryItemResponse])
async def expired_items(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Items ya vencidos."""
    service = PantryService(session)
    return await service.expired_items(current_user.id)


@router.get("/items/{item_id}", response_model=PantryItemResponse)
async def get_pantry_item(
    item_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Obtener un item de la despensa."""
    service = PantryService(session)
    item = await service.get_item(current_user.id, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
    return item


@router.patch("/items/{item_id}", response_model=PantryItemResponse)
async def update_pantry_item(
    item_id: int,
    data: PantryItemUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Actualizar un item de la despensa."""
    service = PantryService(session)
    item = await service.update_item(current_user.id, item_id, data)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
    return item


@router.post("/items/{item_id}/consume", response_model=PantryItemResponse)
async def consume_pantry_item(
    item_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Marcar un item como consumido."""
    service = PantryService(session)
    item = await service.mark_status(current_user.id, item_id, "consumed")
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
    return item


@router.post("/items/{item_id}/waste", response_model=PantryItemResponse)
async def waste_pantry_item(
    item_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Marcar un item como desperdiciado (FOODARA ZERO)."""
    service = PantryService(session)
    item = await service.mark_status(current_user.id, item_id, "wasted")
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
    return item


@router.delete("/items/{item_id}", status_code=status.HTTP_200_OK)
async def delete_pantry_item(
    item_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    """Eliminar un item de la despensa."""
    service = PantryService(session)
    deleted = await service.delete_item(current_user.id, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
    return {"message": "Item eliminado de la despensa"}
