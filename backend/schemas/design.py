"""
Pydantic schemas for Design operations.
"""

from uuid import UUID
from pydantic import BaseModel


class DesignBase(BaseModel):
    """Base schema for Design."""

    name: str
    category_id: UUID
    fabric_id: UUID
    customization: dict


class DesignCreate(DesignBase):
    """Schema for creating a new Design."""

    pass


class Design(DesignBase):
    """Schema for reading Design from database."""

    id: UUID
    user_id: UUID

    class Config:
        orm_mode = True
