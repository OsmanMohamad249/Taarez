"""
Pydantic schemas for User operations.
"""

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from models.roles import UserRole


class UserRegister(BaseModel):
    """Schema for public user registration (customers only)."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    # Role field removed - will default to CUSTOMER in the database model


class UserRegisterWithRole(BaseModel):
    """Schema for admin user registration (with role specification)."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole = UserRole.CUSTOMER


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for token response."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema for user response."""

    id: UUID
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    is_superuser: bool
    role: UserRole
    created_at: datetime

    class Config:
        orm_mode = True
