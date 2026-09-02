"""
FOODARA AI - User Models
Modelos para usuarios y autenticación.
"""

from sqlalchemy import (
    String,
    Boolean,
    Float,
    Column,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.database.base import Base, IDMixin, TimeStampMixin


class User(Base, IDMixin, TimeStampMixin):
    """
    Modelo de usuario FOODARA.
    Información básica del usuario.
    """
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)

    is_active = Column(Boolean, default=True, index=True)
    is_superuser = Column(Boolean, default=False)

    # Relaciones
    preferences = relationship("UserPreference", back_populates="user", uselist=False)
    pantry_items = relationship("PantryItem", back_populates="user")
    shopping_lists = relationship("ShoppingList", back_populates="user")
    purchases = relationship("Purchase", back_populates="user")
    receipts = relationship("Receipt", back_populates="user")
    meal_plans = relationship("MealPlan", back_populates="user")
    conversations = relationship("AIConversation", back_populates="user")
    waste_records = relationship("WasteRecord", back_populates="user")
    achievements = relationship("Achievement", back_populates="user")
    score = relationship("UserScore", back_populates="user", uselist=False)
    households = relationship("HouseholdMember", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"


class UserPreference(Base, IDMixin, TimeStampMixin):
    """
    Preferencias y configuración del usuario.
    Información para personalizar FOODARA.
    """
    __tablename__ = "user_preferences"

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # Configuración básica
    currency = Column(String(3), default="ARS")
    language = Column(String(5), default="es")
    timezone = Column(String(50), default="America/Argentina/Buenos_Aires")

    # Preferencias de compra
    preferred_budget_ars = Column(Float, default=50000)
    people_at_home = Column(Integer, default=2)
    cooking_time_available_minutes = Column(Integer, default=30)

    # Preferencias alimenticias
    vegetarian = Column(Boolean, default=False)
    vegan = Column(Boolean, default=False)
    gluten_free = Column(Boolean, default=False)
    dairy_free = Column(Boolean, default=False)

    # Notificaciones
    email_notifications = Column(Boolean, default=True)
    waste_alerts = Column(Boolean, default=True)
    budget_alerts = Column(Boolean, default=True)

    # Relación
    user = relationship("User", back_populates="preferences")

    def __repr__(self) -> str:
        return f"<UserPreference(user_id={self.user_id})>"
