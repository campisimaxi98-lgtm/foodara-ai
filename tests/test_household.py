"""
FOODARA AI - Household Service Tests
Tests unitarios de hogares (FOODARA HOME).
Usa SQLite async en memoria para no depender de PostgreSQL.
"""

import pytest

from app.models import User
from app.services.household_service import HouseholdService
from app.schemas.household import HouseholdCreate
from app.core.security import hash_password


async def _make_user(session, email, username) -> User:
    user = User(
        email=email,
        username=username,
        hashed_password=hash_password("SecurePass123!"),
    )
    session.add(user)
    await session.flush()
    return user


@pytest.mark.asyncio
@pytest.mark.unit
async def test_create_household_sets_owner(test_db):
    """Al crear un hogar, el creador queda como owner."""
    user = await _make_user(test_db, "owner@foodara.ar", "owneruser")
    service = HouseholdService(test_db)

    household = await service.create_household(
        user, HouseholdCreate(name="Mi Casa")
    )

    assert household.id is not None
    role = await service.get_member_role(user.id, household.id)
    assert role == "owner"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_is_member_and_list(test_db):
    """Verificar membresía y listar hogares del usuario."""
    user = await _make_user(test_db, "member@foodara.ar", "memberuser")
    service = HouseholdService(test_db)

    household = await service.create_household(
        user, HouseholdCreate(name="Hogar Test")
    )

    assert await service.is_member(user.id, household.id) is True
    assert await service.is_member(user.id + 999, household.id) is False
    assert len(await service.list_user_households(user.id)) == 1


@pytest.mark.asyncio
@pytest.mark.unit
async def test_add_duplicate_member_raises(test_db):
    """No se puede agregar dos veces el mismo miembro."""
    owner = await _make_user(test_db, "o@foodara.ar", "owneru")
    service = HouseholdService(test_db)
    household = await service.create_household(owner, HouseholdCreate(name="Casa"))

    with pytest.raises(ValueError):
        await service.add_member(household.id, owner.id, role="member")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_update_household_whitelist(test_db):
    """Actualizar solo campos permitidos."""
    owner = await _make_user(test_db, "u@foodara.ar", "updater")
    service = HouseholdService(test_db)
    household = await service.create_household(owner, HouseholdCreate(name="Original"))

    from app.schemas.household import HouseholdUpdate

    updated = await service.update_household(
        household, HouseholdUpdate(name="Renombrado", budget_ars=10000)
    )
    assert updated.name == "Renombrado"
    assert updated.budget_ars == 10000
