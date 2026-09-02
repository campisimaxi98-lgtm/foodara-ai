"""
FOODARA AI - Household Schemas
Schemas Pydantic para hogares (FOODARA HOME).
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class HouseholdMemberCreate(BaseModel):
    """Schema para agregar un miembro a un hogar."""
    user_id: int
    role: str = Field(default="member", pattern="^(owner|admin|member)$")


class HouseholdCreate(BaseModel):
    """Schema para crear un hogar."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    budget_ars: Optional[float] = Field(default=None, ge=0)
    people_count: int = Field(default=1, ge=1, le=100)


class HouseholdUpdate(BaseModel):
    """Schema para actualizar un hogar."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    budget_ars: Optional[float] = Field(default=None, ge=0)
    people_count: Optional[int] = Field(default=None, ge=1, le=100)
    is_active: Optional[bool] = None


class HouseholdMemberResponse(BaseModel):
    """Schema de respuesta de un miembro del hogar."""
    id: int
    household_id: int
    user_id: int
    role: str
    joined_at: datetime

    class Config:
        from_attributes = True


class HouseholdResponse(BaseModel):
    """Schema de respuesta de un hogar."""
    id: int
    name: str
    description: Optional[str]
    budget_ars: Optional[float]
    currency: str
    people_count: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    members: List[HouseholdMemberResponse] = []

    class Config:
        from_attributes = True
