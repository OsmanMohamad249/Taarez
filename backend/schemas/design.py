"""
Pydantic schemas for Design operations.
"""

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class DesignCreate(BaseModel):
    """Schema for creating a design."""

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    style_type: Optional[str] = None
    price: float = Field(..., gt=0)
    image_url: Optional[str] = None
    category_id: Optional[UUID] = None


class DesignUpdate(BaseModel):
    """Schema for updating a design."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    style_type: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    image_url: Optional[str] = None
    category_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class DesignResponse(BaseModel):
    """Schema for design response."""

    id: UUID
    title: str
    description: Optional[str] = None
    style_type: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    designer_id: UUID
    category_id: Optional[UUID] = None
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True
