"""
FOODARA AI - Pantry Service Tests
Tests unitarios de la despensa (FOODARA HOME).
Usa SQLite async en memoria para no depender de PostgreSQL.
"""

import pytest
from datetime import datetime, timedelta, timezone

from app.models import User
from app.services.pantry_service import PantryService
from app.schemas.pantry import PantryItemCreate, PantryItemUpdate
from app.core.security import hash_password


async def _make_user(session, email="pantry@foodara.ar", username="pantryuser") -> User:
    user = User(
        email=email,
        username=username,
        hashed_password=hash_password("SecurePass123!"),
    )
    session.add(user)
    await session.flush()
    return user


def _ago(days: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days)


def _ahead(days: int) -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=days)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_add_pantry_item_creates_food(test_db):
    """Agregar un item sin food_id debe resolver/crear el alimento."""
    user = await _make_user(test_db)
    service = PantryService(test_db)

    item = await service.add_item(
        user,
        PantryItemCreate(food_name="Leche Entera", quantity=2.0, unit="L"),
    )

    assert item.food_name == "Leche Entera"
    assert item.food_id is not None
    assert item.user_id == user.id
    assert item.status == "available"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_expiring_items_only_returns_soon(test_db):
    """Solo items próximos a vencer dentro del horizonte."""
    user = await _make_user(test_db)
    service = PantryService(test_db)

    await service.add_item(
        user,
        PantryItemCreate(food_name="Yogur", quantity=1.0, unit="u", expiry_date=_ahead(2)),
    )
    await service.add_item(
        user,
        PantryItemCreate(food_name="Atún", quantity=1.0, unit="u", expiry_date=_ahead(200)),
    )

    expiring = await service.expiring_items(user.id, days=7)
    names = [i.food_name for i in expiring]
    assert "Yogur" in names
    assert "Atún" not in names


@pytest.mark.asyncio
@pytest.mark.unit
async def test_expired_items(test_db):
    """Items ya vencidos."""
    user = await _make_user(test_db)
    service = PantryService(test_db)

    await service.add_item(
        user,
        PantryItemCreate(food_name="Pan", quantity=1.0, unit="u", expiry_date=_ago(3)),
    )
    await service.add_item(
        user,
        PantryItemCreate(food_name="Arroz", quantity=1.0, unit="kg", expiry_date=_ahead(30)),
    )

    expired = await service.expired_items(user.id)
    names = [i.food_name for i in expired]
    assert "Pan" in names
    assert "Arroz" not in names


@pytest.mark.asyncio
@pytest.mark.unit
async def test_mark_status_consume_and_waste(test_db):
    """Cambiar estado a consumido y desperdiciado."""
    user = await _make_user(test_db)
    service = PantryService(test_db)

    item = await service.add_item(
        user, PantryItemCreate(food_name="Queso", quantity=1.0, unit="u")
    )

    consumed = await service.mark_status(user.id, item.id, "consumed")
    assert consumed.status == "consumed"

    wasted = await service.mark_status(user.id, item.id, "wasted")
    assert wasted.status == "wasted"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_summary_counts(test_db):
    """Resumen determinístico de la despensa."""
    user = await _make_user(test_db)
    service = PantryService(test_db)

    await service.add_item(user, PantryItemCreate(food_name="A", quantity=1.0, unit="u"))
    await service.add_item(user, PantryItemCreate(food_name="B", quantity=1.0, unit="u"))
    items = await service.list_items(user.id)
    await service.mark_status(user.id, items[0].id, "wasted")

    summary = await service.get_summary(user.id)
    assert summary.total_items == 2
    assert summary.items_available == 1
    assert summary.items_wasted == 1
    assert summary.items_consumed == 0


@pytest.mark.asyncio
@pytest.mark.unit
async def test_item_ownership_enforced(test_db):
    """Un usuario no puede ver los items de otro."""
    user_a = await _make_user(test_db, email="a@foodara.ar", username="usera")
    user_b = await _make_user(test_db, email="b@foodara.ar", username="userb")

    service = PantryService(test_db)
    await service.add_item(user_a, PantryItemCreate(food_name="Secreto", quantity=1.0, unit="u"))

    # user_b no debe ver los items de user_a
    assert await service.get_item(user_b.id, 1) is None
    assert await service.list_items(user_b.id) == []


@pytest.mark.asyncio
@pytest.mark.unit
async def test_update_item_whitelist(test_db):
    """Actualizar solo campos permitidos."""
    user = await _make_user(test_db)
    service = PantryService(test_db)

    item = await service.add_item(
        user, PantryItemCreate(food_name="Aceite", quantity=1.0, unit="L")
    )

    updated = await service.update_item(
        user.id,
        item.id,
        PantryItemUpdate(status="available", quantity=3.0),
    )

    assert updated.quantity == 3.0
