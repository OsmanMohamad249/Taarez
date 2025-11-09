"""
Pydantic schemas for Category operations.
"""

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    """Schema for creating a category."""

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = True


class CategoryUpdate(BaseModel):
    """Schema for updating a category."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryResponse(BaseModel):
    """Schema for category response."""

    id: UUID
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True
