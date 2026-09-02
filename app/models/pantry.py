"""
FOODARA AI - Pantry Models
Modelos para despensa digital y alimentos.
"""

from sqlalchemy import (
    String,
    Float,
    Integer,
    Column,
    ForeignKey,
    DateTime,
    Text,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database.base import Base, IDMixin, TimeStampMixin, utcnow


class Food(Base, IDMixin, TimeStampMixin):
    """
    Catálogo de alimentos FOODARA.
    Información centralizada de alimentos.
    """
    __tablename__ = "foods"
    __table_args__ = (
        UniqueConstraint("name", "category", name="uq_food_name_category"),
    )

    name = Column(String(255), index=True, nullable=False)
    category = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)

    # Información nutricional
    nutrition_info = relationship(
        "NutritionInfo",
        back_populates="food",
        uselist=False
    )

    # Alimentos en despensa
    pantry_items = relationship("PantryItem", back_populates="food")

    def __repr__(self) -> str:
        return f"<Food(id={self.id}, name={self.name}, category={self.category})>"


class NutritionInfo(Base, IDMixin, TimeStampMixin):
    """
    Información nutricional por alimento.
    Por 100g de producto.
    """
    __tablename__ = "nutrition_info"
    __table_args__ = (
        UniqueConstraint("food_id", name="uq_nutrition_food_id"),
    )

    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)

    calories = Column(Float, default=0)
    protein_g = Column(Float, default=0)
    carbs_g = Column(Float, default=0)
    fat_g = Column(Float, default=0)
    fiber_g = Column(Float, default=0)

    # Relación
    food = relationship("Food", back_populates="nutrition_info")

    def __repr__(self) -> str:
        return f"<NutritionInfo(food_id={self.food_id}, calories={self.calories})>"


class PantryItem(Base, IDMixin, TimeStampMixin):
    """
    Despensa digital del usuario/hogar.
    Items que el usuario tiene en casa.
    """
    __tablename__ = "pantry_items"
    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="ck_pantry_quantity_positive",
        ),
        CheckConstraint(
            "status IN ('available', 'consumed', 'wasted')",
            name="ck_pantry_status",
        ),
    )

    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    household_id = Column(
        Integer,
        ForeignKey("households.id"),
        index=True,
        nullable=True,
    )
    food_id = Column(Integer, ForeignKey("foods.id"), index=True, nullable=True)
    food_name = Column(String(255), nullable=True)

    quantity = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)  # kg, g, L, ml, unidades

    # Precio y marcas para tracking económico
    brand = Column(String(100), nullable=True)
    price_ars = Column(Float, nullable=True)

    # Fechas importantes
    purchase_date = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    expiry_date = Column(DateTime(timezone=True), index=True, nullable=True)
    actual_expiry_date = Column(DateTime(timezone=True), nullable=True)

    # Ubicación y estado
    location = Column(String(100), nullable=True)
    status = Column(String(20), index=True, default="available")  # available, consumed, wasted

    notes = Column(Text, nullable=True)

    # Relaciones
    user = relationship("User", back_populates="pantry_items")
    household = relationship("Household", back_populates="pantry_items")
    food = relationship("Food", back_populates="pantry_items")

    def __repr__(self) -> str:
        return f"<PantryItem(id={self.id}, user_id={self.user_id}, quantity={self.quantity}{self.unit})>"
