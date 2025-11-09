"""
Pydantic schemas for Fabric operations.
"""

from uuid import UUID
from pydantic import BaseModel


class FabricBase(BaseModel):
    """Base schema for Fabric."""

    name: str
    description: str | None = None
    image_url: str | None = None
    price_per_meter: float | None = None
    category_id: UUID


class Fabric(FabricBase):
    """Schema for reading Fabric from database."""

    id: UUID

    class Config:
        orm_mode = True
