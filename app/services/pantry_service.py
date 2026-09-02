"""
FOODARA AI - Pantry Service
Lógica de negocio de la despensa digital (FOODARA HOME).

Todas las métricas de inventario, vencimientos y valores son
cálculos determinísticos, NO dependen de IA generativa.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from app.models import PantryItem, Food, User
from app.schemas.pantry import (
    PantryItemCreate,
    PantryItemUpdate,
    PantrySummary,
)


logger = logging.getLogger(__name__)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class PantryService:
    """Servicio para la gestión de la despensa."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _resolve_food(self, data: PantryItemCreate) -> tuple[Optional[int], str]:
        """
        Resolver el alimento a usar. Devuelve (food_id, food_name).
        Si food_id existe usa el catálogo; sino busca/crea una entrada de catálogo.
        """
        food_name = (data.food_name or "").strip()

        if data.food_id is not None:
            result = await self.session.execute(
                select(Food).where(Food.id == data.food_id)
            )
            food = result.scalar_one_or_none()
            if not food:
                raise ValueError("Alimento no encontrado en el catálogo")
            return food.id, food.name

        if not food_name:
            raise ValueError("Debe indicar food_id o food_name")

        # Buscar alimento existente por nombre (ignorando mayúsculas)
        result = await self.session.execute(
            select(Food).where(func.lower(Food.name) == food_name.lower())
        )
        food = result.scalar_one_or_none()

        if not food:
            food = Food(name=food_name, category="general")
            self.session.add(food)
            await self.session.flush()

        return food.id, food.name

    async def add_item(self, user: User, data: PantryItemCreate) -> PantryItem:
        """Agregar un item a la despensa del usuario."""
        food_id, food_name = await self._resolve_food(data)

        item = PantryItem(
            user_id=user.id,
            food_id=food_id,
            food_name=food_name,
            quantity=data.quantity,
            unit=data.unit,
            brand=data.brand,
            price_ars=data.price_ars,
            purchase_date=data.purchase_date or _utcnow(),
            expiry_date=data.expiry_date,
            location=data.location,
            notes=data.notes,
        )
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)

        logger.info(f"Item agregado a despensa: {food_name} (user={user.id})")
        return item

    async def list_items(
        self,
        user_id: int,
        status: Optional[str] = None,
        location: Optional[str] = None,
    ) -> List[PantryItem]:
        """Listar items de la despensa del usuario."""
        query = select(PantryItem).where(PantryItem.user_id == user_id)

        if status:
            query = query.where(PantryItem.status == status)
        if location:
            query = query.where(PantryItem.location == location)

        query = query.order_by(PantryItem.expiry_date.asc())
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_item(self, user_id: int, item_id: int) -> Optional[PantryItem]:
        """Obtener un item verificando pertenencia al usuario."""
        result = await self.session.execute(
            select(PantryItem).where(
                PantryItem.id == item_id,
                PantryItem.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def update_item(
        self,
        user_id: int,
        item_id: int,
        data: PantryItemUpdate,
    ) -> Optional[PantryItem]:
        """Actualizar un item de la despensa."""
        item = await self.get_item(user_id, item_id)
        if not item:
            return None

        allowed = {
            "quantity", "unit", "brand", "price_ars", "purchase_date",
            "expiry_date", "location", "status", "notes",
        }
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field in allowed:
                setattr(item, field, value)

        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)

        logger.info(f"Item de despensa actualizado: {item_id}")
        return item

    async def delete_item(self, user_id: int, item_id: int) -> bool:
        """Eliminar un item de la despensa."""
        item = await self.get_item(user_id, item_id)
        if not item:
            return False

        await self.session.delete(item)
        await self.session.commit()

        logger.info(f"Item de despensa eliminado: {item_id}")
        return True

    async def expiring_items(
        self,
        user_id: int,
        days: int = 7,
        include_expired: bool = False,
    ) -> List[PantryItem]:
        """
        Items próximos a vencer dentro de `days` días,
        opcionalmente incluyendo los ya vencidos.
        Solo items en estado "available".
        """
        now = _utcnow()
        horizon = now + timedelta(days=days)

        conditions = [
            PantryItem.user_id == user_id,
            PantryItem.status == "available",
            PantryItem.expiry_date.isnot(None),
            PantryItem.expiry_date <= horizon,
        ]
        if not include_expired:
            conditions.append(PantryItem.expiry_date >= now)

        query = (
            select(PantryItem)
            .where(*conditions)
            .order_by(PantryItem.expiry_date.asc())
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def expired_items(self, user_id: int) -> List[PantryItem]:
        """Items ya vencidos (estado available)."""
        now = _utcnow()
        result = await self.session.execute(
            select(PantryItem).where(
                PantryItem.user_id == user_id,
                PantryItem.status == "available",
                PantryItem.expiry_date.isnot(None),
                PantryItem.expiry_date < now,
            ).order_by(PantryItem.expiry_date.asc())
        )
        return list(result.scalars().all())

    async def mark_status(self, user_id: int, item_id: int, status: str) -> Optional[PantryItem]:
        """Cambiar el estado de un item (consumed / wasted / available)."""
        item = await self.get_item(user_id, item_id)
        if not item:
            return None

        item.status = status
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def get_summary(self, user_id: int) -> PantrySummary:
        """Resumen determinístico de la despensa."""
        items = await self.list_items(user_id)

        available = [i for i in items if i.status == "available"]
        consumed = [i for i in items if i.status == "consumed"]
        wasted = [i for i in items if i.status == "wasted"]

        now = _utcnow()
        expiring = [
            i for i in available
            if i.expiry_date is not None
            and i.expiry_date >= now
            and i.expiry_date <= now + timedelta(days=7)
        ]
        expired = [
            i for i in available
            if i.expiry_date is not None and i.expiry_date < now
        ]

        def total_value(row_list: List[PantryItem]) -> float:
            return sum((i.price_ars or 0.0) for i in row_list)

        return PantrySummary(
            total_items=len(items),
            items_available=len(available),
            items_consumed=len(consumed),
            items_wasted=len(wasted),
            expiry_soon_count=len(expiring),
            expired_count=len(expired),
            estimated_value_ars=round(total_value(available), 2),
            estimated_expiring_value_ars=round(total_value(expiring) + total_value(expired), 2),
        )
