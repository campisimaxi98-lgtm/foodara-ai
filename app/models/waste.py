"""
FOODARA AI - Waste Models
Modelos para registro y análisis de desperdicios.
"""

from sqlalchemy import String, Float, Integer, Column, ForeignKey, DateTime, Text

from app.database.base import Base, IDMixin, TimeStampMixin, utcnow


class WasteRecord(Base, IDMixin, TimeStampMixin):
    """
    Registro de desperdicio de un usuario.
    Alimento que fue desechado.
    """
    __tablename__ = "waste_records"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pantry_item_id = Column(Integer, ForeignKey("pantry_items.id"), nullable=True)

    # Información del alimento
    food_name = Column(String(255), nullable=False)
    quantity_wasted = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)

    # Razón del desperdicio
    waste_reason = Column(String(100), nullable=True)
    # opciones: expired, forgotten, damaged, refused, other

    # Fecha y contexto
    waste_date = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    estimated_cost_ars = Column(Float, nullable=True)

    notes = Column(Text, nullable=True)

    # Relaciones
    user = relationship("User", back_populates="waste_records")

    def __repr__(self) -> str:
        return f"<WasteRecord(id={self.id}, user_id={self.user_id}, food={self.food_name})>"
