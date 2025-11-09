"""
Pydantic schemas for Category operations.
"""

from uuid import UUID
from pydantic import BaseModel


class CategoryBase(BaseModel):
    """Base schema for Category."""

    name: str
    description: str | None = None


class Category(CategoryBase):
    """Schema for reading Category from database."""

    id: UUID

    class Config:
        orm_mode = True
