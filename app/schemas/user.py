"""
FOODARA AI - User Schemas
Pydantic schemas para endpoints de usuarios.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schema para crear un nuevo usuario."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema para actualizar usuario."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(BaseModel):
    """Schema de respuesta para usuario."""
    id: int
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenRequest(BaseModel):
    """Schema para login."""
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    """Schema para renovar el access token con un refresh token."""
    refresh_token: str


class AccessTokenResponse(BaseModel):
    """Schema de respuesta para renovar token."""
    access_token: str
    token_type: str = "bearer"


class TokenResponse(BaseModel):
    """Schema para respuesta de token."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserPreferenceResponse(BaseModel):
    """Schema de preferencias del usuario."""
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


class UserProfileResponse(BaseModel):
    """Schema completo del perfil del usuario."""
    user: UserResponse
    preferences: UserPreferenceResponse

    class Config:
        from_attributes = True
