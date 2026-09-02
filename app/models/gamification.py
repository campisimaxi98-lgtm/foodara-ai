"""
FOODARA AI - Gamification Models
Modelos para sistema de puntos y logros.
"""

from sqlalchemy import (
    String,
    Float,
    Integer,
    Column,
    ForeignKey,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import relationship

from app.database.base import Base, IDMixin, TimeStampMixin


class UserScore(Base, IDMixin, TimeStampMixin):
    """
    Puntuación de FOODARA del usuario.
    Métrica de comportamiento dentro de la app.
    """
    __tablename__ = "user_scores"

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # Scores por categoría (0-100)
    shopping_score = Column(Float, default=50)
    planning_score = Column(Float, default=50)
    waste_reduction_score = Column(Float, default=50)
    budget_score = Column(Float, default=50)

    # Puntuación total
    total_score = Column(Float, default=50)

    # Experiencia y nivel
    experience_points = Column(Integer, default=0)
    level = Column(Integer, default=1)

    # Relación
    user = relationship("User", back_populates="score")

    def __repr__(self) -> str:
        return f"<UserScore(user_id={self.user_id}, total_score={self.total_score})>"


class Achievement(Base, IDMixin, TimeStampMixin):
    """
    Logro desbloqueado por un usuario.
    Insignia o trofeo dentro de FOODARA.
    """
    __tablename__ = "achievements"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Información del logro
    achievement_type = Column(String(100), nullable=False, index=True)
    # Examples: first_week, zero_waste, smart_shopping, chef_foodara

    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)

    # Estado
    is_unlocked = Column(Boolean, default=False)
    unlock_date = Column(DateTime, nullable=True)

    # Bonus
    bonus_points = Column(Integer, default=0)

    # Relación
    user = relationship("User", back_populates="achievements")

    def __repr__(self) -> str:
        return f"<Achievement(user_id={self.user_id}, type={self.achievement_type})>"
