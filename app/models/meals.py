"""
FOODARA AI - Meal Models
Modelos para planes de comidas, recetas y menús.
"""

from sqlalchemy import String, Float, Integer, Column, ForeignKey, DateTime, Text, Boolean

from app.database.base import Base, IDMixin, TimeStampMixin, utcnow


class MealPlan(Base, IDMixin, TimeStampMixin):
    """
    Plan de comidas del usuario.
    Un usuario puede tener múltiples planes.
    """
    __tablename__ = "meal_plans"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Período del plan
    start_date = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)

    # Presupuesto y configuración
    budget_ars = Column(Float, nullable=True)
    people_count = Column(Integer, default=2)

    is_active = Column(Boolean, default=True)

    # Relaciones
    user = relationship("User", back_populates="meal_plans")
    meals = relationship("Meal", back_populates="meal_plan", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<MealPlan(id={self.id}, user_id={self.user_id}, name={self.name})>"


class Meal(Base, IDMixin, TimeStampMixin):
    """
    Comida individual dentro de un plan.
    Breakfast, lunch, dinner, snack, etc.
    """
    __tablename__ = "meals"

    meal_plan_id = Column(Integer, ForeignKey("meal_plans.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)

    meal_type = Column(String(50), nullable=False)  # breakfast, lunch, dinner, snack
    meal_date = Column(DateTime, nullable=False)

    servings = Column(Integer, default=1)
    estimated_cost_ars = Column(Float, nullable=True)

    # Relaciones
    meal_plan = relationship("MealPlan", back_populates="meals")
    recipe = relationship("Recipe", back_populates="meals")

    def __repr__(self) -> str:
        return f"<Meal(id={self.id}, meal_type={self.meal_type})>"


class Recipe(Base, IDMixin, TimeStampMixin):
    """
    Receta en el sistema FOODARA.
    Puede ser generada por IA o creada por usuario.
    """
    __tablename__ = "recipes"

    name = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)

    # Información de preparación
    cooking_time_minutes = Column(Integer, default=30)
    difficulty = Column(String(50), default="medio")  # facil, medio, dificil
    servings = Column(Integer, default=4)

    # Costo
    estimated_cost_ars = Column(Float, nullable=True)

    # Información nutricional
    calories_per_serving = Column(Float, nullable=True)

    # Almacenamiento
    is_generated_by_ai = Column(Boolean, default=False)

    # Relaciones
    ingredients = relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )
    meals = relationship("Meal", back_populates="recipe")

    def __repr__(self) -> str:
        return f"<Recipe(id={self.id}, name={self.name})>"


class RecipeIngredient(Base, IDMixin, TimeStampMixin):
    """
    Ingrediente de una receta.
    Vincula recetas con sus ingredientes.
    """
    __tablename__ = "recipe_ingredients"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=True)

    # Información del ingrediente
    ingredient_name = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)

    is_optional = Column(Boolean, default=False)

    # Relaciones
    recipe = relationship("Recipe", back_populates="ingredients")

    def __repr__(self) -> str:
        return f"<RecipeIngredient(recipe_id={self.recipe_id}, ingredient={self.ingredient_name})>"
