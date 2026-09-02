"""
FOODARA AI - Schemas
Centraliza todos los schemas Pydantic.
"""

from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    TokenRequest,
    TokenResponse,
    UserPreferenceResponse,
    UserProfileResponse,
)

from app.schemas.preference import (
    PreferenceBase,
    PreferenceCreate,
    PreferenceUpdate,
    PreferenceResponse,
    FoodaryProfileCreate,
    FoodaryProfileResponse,
)

from app.schemas.household import (
    HouseholdCreate,
    HouseholdUpdate,
    HouseholdResponse,
    HouseholdMemberCreate,
    HouseholdMemberResponse,
)

from app.schemas.pantry import (
    FoodCreate,
    FoodResponse,
    PantryItemCreate,
    PantryItemUpdate,
    PantryItemResponse,
    PantrySummary,
)

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "TokenRequest",
    "TokenResponse",
    "UserPreferenceResponse",
    "UserProfileResponse",
    "PreferenceBase",
    "PreferenceCreate",
    "PreferenceUpdate",
    "PreferenceResponse",
    "FoodaryProfileCreate",
    "FoodaryProfileResponse",
    "HouseholdCreate",
    "HouseholdUpdate",
    "HouseholdResponse",
    "HouseholdMemberCreate",
    "HouseholdMemberResponse",
    "FoodCreate",
    "FoodResponse",
    "PantryItemCreate",
    "PantryItemUpdate",
    "PantryItemResponse",
    "PantrySummary",
]
