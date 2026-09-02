"""
FOODARA AI - Household Models
Modelos de hogares (FOODARA HOME).

Un hogar agrupa usuarios que comparten despensa, compras, presupuesto,
menú, inventario y estadísticas.
"""

from sqlalchemy import (
    String,
    Integer,
    Column,
    ForeignKey,
    DateTime,
    Text,
    Float,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database.base import Base, IDMixin, TimeStampMixin, utcnow


class Household(Base, IDMixin, TimeStampMixin):
    """
    Hogar dentro de FOODARA.
    Núcleo del módulo FOODARA HOME: agrupa usuarios y recursos compartidos.
    """

    __tablename__ = "households"

    name = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)

    # Presupuesto compartido del hogar (ARS)
    budget_ars = Column(Float, nullable=True)
    currency = Column(String(3), default="ARS")

    # Personas que viven en el hogar
    people_count = Column(Integer, default=1)

    # Estado
    is_active = Column(Boolean, default=True)

    # Relaciones
    members = relationship(
        "HouseholdMember",
        back_populates="household",
        cascade="all, delete-orphan",
    )
    pantry_items = relationship("PantryItem", back_populates="household")

    def __repr__(self) -> str:
        return f"<Household(id={self.id}, name={self.name}, people={self.people_count})>"


class HouseholdMember(Base, IDMixin, TimeStampMixin):
    """
    Miembro de un hogar.
    Relaciona un usuario con un hogar y define su rol.
    """

    __tablename__ = "household_members"
    __table_args__ = (
        UniqueConstraint("household_id", "user_id", name="uq_household_member"),
    )

    household_id = Column(Integer, ForeignKey("households.id"), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)

    # Roles: owner | admin | member
    role = Column(String(20), default="member")

    joined_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relaciones
    household = relationship("Household", back_populates="members")
    user = relationship("User", back_populates="households")

    def __repr__(self) -> str:
        return (
            f"<HouseholdMember(household_id={self.household_id}, "
            f"user_id={self.user_id}, role={self.role})>"
        )
