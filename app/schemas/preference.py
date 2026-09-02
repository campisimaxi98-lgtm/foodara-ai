"""
FOODARA AI - Preference Schemas
Schemas Pydantic para preferencias del usuario.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class PreferenceBase(BaseModel):
    """Base para preferencias."""
    currency: str = Field(default="ARS", min_length=3, max_length=3)
    language: str = Field(default="es", min_length=2, max_length=5)
    timezone: str = Field(default="America/Argentina/Buenos_Aires")
    preferred_budget_ars: float = Field(default=50000, ge=0)
    people_at_home: int = Field(default=2, ge=1, le=20)
    cooking_time_available_minutes: int = Field(default=30, ge=5, le=480)


class PreferenceCreate(PreferenceBase):
    """Schema para crear preferencias."""
    vegetarian: bool = False
    vegan: bool = False
    gluten_free: bool = False
    dairy_free: bool = False
    email_notifications: bool = True
    waste_alerts: bool = True
    budget_alerts: bool = True


class PreferenceUpdate(BaseModel):
    """Schema para actualizar preferencias."""
    currency: Optional[str] = Field(default=None, min_length=3, max_length=3)
    language: Optional[str] = Field(default=None, min_length=2, max_length=5)
    timezone: Optional[str] = None
    preferred_budget_ars: Optional[float] = Field(default=None, ge=0)
    people_at_home: Optional[int] = Field(default=None, ge=1, le=20)
    cooking_time_available_minutes: Optional[int] = Field(default=None, ge=5, le=480)
    vegetarian: Optional[bool] = None
    vegan: Optional[bool] = None
    gluten_free: Optional[bool] = None
    dairy_free: Optional[bool] = None
    email_notifications: Optional[bool] = None
    waste_alerts: Optional[bool] = None
    budget_alerts: Optional[bool] = None


class PreferenceResponse(BaseModel):
    """Schema de respuesta de preferencias."""
    id: int
    user_id: int
    currency: str
    language: str
    timezone: str
    preferred_budget_ars: float
    people_at_home: int
    cooking_time_available_minutes: int
    vegetarian: bool
    vegan: bool
    gluten_free: bool
    dairy_free: bool
    email_notifications: bool
    waste_alerts: bool
    budget_alerts: bool

    class Config:
        from_attributes = True


class FoodaryProfileCreate(BaseModel):
    """Schema para crear perfil FOODARA completo."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    preferences: PreferenceCreate


class FoodaryProfileResponse(BaseModel):
    """Schema de respuesta del perfil FOODARA."""
    id: int
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    preferences: PreferenceResponse

    class Config:
        from_attributes = True
