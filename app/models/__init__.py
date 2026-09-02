"""
FOODARA AI - Models
Centraliza todos los modelos SQLAlchemy.
"""

from app.models.user import User, UserPreference
from app.models.household import Household, HouseholdMember
from app.models.pantry import PantryItem, Food, NutritionInfo
from app.models.shopping import ShoppingList, ShoppingListItem, Product
from app.models.purchases import Purchase
from app.models.receipts import Receipt, ReceiptItem
from app.models.meals import MealPlan, Meal, Recipe, RecipeIngredient
from app.models.ai_chat import AIConversation, AIMessage
from app.models.waste import WasteRecord
from app.models.gamification import Achievement, UserScore

__all__ = [
    "User",
    "UserPreference",
    "Household",
    "HouseholdMember",
    "PantryItem",
    "Food",
    "NutritionInfo",
    "ShoppingList",
    "ShoppingListItem",
    "Product",
    "Purchase",
    "Receipt",
    "ReceiptItem",
    "MealPlan",
    "Meal",
    "Recipe",
    "RecipeIngredient",
    "AIConversation",
    "AIMessage",
    "WasteRecord",
    "Achievement",
    "UserScore",
]
