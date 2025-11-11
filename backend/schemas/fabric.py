"""
Pydantic schemas for Fabric operations.
"""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class FabricCreate(BaseModel):
    """Schema for creating a fabric."""

    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    image_url: Optional[str] = None
    base_price: float = Field(..., gt=0)


class FabricUpdate(BaseModel):
    """Schema for updating a fabric."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    image_url: Optional[str] = None
    base_price: Optional[float] = Field(None, gt=0)


class FabricResponse(BaseModel):
    """Schema for fabric response."""

    id: UUID
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    base_price: float

    class Config:
        orm_mode = True
