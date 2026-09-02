"""
FOODARA AI - Database Base
Base declarativa para todos los modelos.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Boolean,
    func,
)


def utcnow() -> datetime:
    """Retorna la hora UTC actual timezone-aware."""
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    """Base declarativa moderna para todos los modelos."""


class TimeStampMixin:
    """
    Mixin que agrega timestamps a todos los modelos.
    created_at y updated_at se actualizan automáticamente.
    """

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=utcnow,
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )


class IDMixin:
    """Mixin que agrega ID primario."""

    id = Column(Integer, primary_key=True, index=True)


class SoftDeleteMixin:
    """
    Mixin de borrado lógico (soft delete).
    Permite "eliminar" filas preservando el dato en la BD para auditoría.
    """

    deleted_at = Column(DateTime(timezone=True), nullable=True)

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
