"""
Pydantic schemas for Design operations.
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class DesignCreate(BaseModel):
    """Schema for creating a design."""

    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    base_image_url: Optional[str] = None
    base_price: float = Field(..., gt=0)
    customization_rules: Optional[Dict[str, Any]] = None
    available_fabric_ids: Optional[List[UUID]] = None
    available_color_ids: Optional[List[UUID]] = None

    # Legacy fields for backward compatibility
    style_type: Optional[str] = None
    category_id: Optional[UUID] = None


class DesignUpdate(BaseModel):
    """Schema for updating a design."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    base_image_url: Optional[str] = None
    base_price: Optional[float] = Field(None, gt=0)
    customization_rules: Optional[Dict[str, Any]] = None
    available_fabric_ids: Optional[List[UUID]] = None
    available_color_ids: Optional[List[UUID]] = None

    # Legacy fields for backward compatibility
    style_type: Optional[str] = None
    category_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class DesignResponse(BaseModel):
    """Schema for design response."""

    id: UUID
    name: str
    description: Optional[str] = None
    base_image_url: Optional[str] = None
    base_price: float
    owner_id: UUID
    customization_rules: Optional[Dict[str, Any]] = None

    # Legacy fields for backward compatibility
    style_type: Optional[str] = None
    category_id: Optional[UUID] = None
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True
