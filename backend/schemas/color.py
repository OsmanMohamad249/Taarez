"""
Pydantic schemas for Color operations.
"""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class ColorCreate(BaseModel):
    """Schema for creating a color."""

    name: str = Field(..., min_length=1, max_length=100)
    hex_code: str = Field(..., min_length=4, max_length=7, regex=r"^#[0-9A-Fa-f]{3,6}$")


class ColorUpdate(BaseModel):
    """Schema for updating a color."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    hex_code: Optional[str] = Field(
        None, min_length=4, max_length=7, regex=r"^#[0-9A-Fa-f]{3,6}$"
    )


class ColorResponse(BaseModel):
    """Schema for color response."""

    id: UUID
    name: str
    hex_code: str

    class Config:
        orm_mode = True
