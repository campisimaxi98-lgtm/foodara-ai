"""
FOODARA AI - Pantry Schemas
Schemas Pydantic para la despensa digital (FOODARA HOME).
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FoodCreate(BaseModel):
    """Schema para crear un alimento del catálogo."""
    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class FoodResponse(BaseModel):
    """Schema de respuesta de un alimento."""
    id: int
    name: str
    category: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class PantryItemCreate(BaseModel):
    """Schema para agregar un item a la despensa."""
    food_id: Optional[int] = None
    food_name: Optional[str] = Field(default=None, max_length=255)
    quantity: float = Field(..., gt=0)
    unit: str = Field(..., min_length=1, max_length=50)
    brand: Optional[str] = Field(default=None, max_length=100)
    price_ars: Optional[float] = Field(default=None, ge=0)
    purchase_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    location: Optional[str] = Field(default=None, max_length=100)
    notes: Optional[str] = None


class PantryItemUpdate(BaseModel):
    """Schema para actualizar un item de la despensa."""
    quantity: Optional[float] = Field(default=None, gt=0)
    unit: Optional[str] = Field(default=None, min_length=1, max_length=50)
    brand: Optional[str] = Field(default=None, max_length=100)
    price_ars: Optional[float] = Field(default=None, ge=0)
    purchase_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    location: Optional[str] = Field(default=None, max_length=100)
    status: Optional[str] = Field(
        default=None, pattern="^(available|consumed|wasted)$"
    )
    notes: Optional[str] = None


class PantryItemResponse(BaseModel):
    """Schema de respuesta de un item de la despensa."""
    id: int
    user_id: int
    household_id: Optional[int]
    food_id: Optional[int]
    food_name: Optional[str] = None
    quantity: float
    unit: str
    brand: Optional[str]
    price_ars: Optional[float]
    purchase_date: Optional[datetime]
    expiry_date: Optional[datetime]
    location: Optional[str]
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PantrySummary(BaseModel):
    """Resumen de la despensa (FOODARA HOME)."""
    total_items: int
    items_available: int
    items_consumed: int
    items_wasted: int
    expiry_soon_count: int
    expired_count: int
    estimated_value_ars: float
    estimated_expiring_value_ars: float
