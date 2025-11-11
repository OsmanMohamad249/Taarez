"""
Schemas package.
"""

from schemas.user import UserRegister, UserLogin, Token, UserResponse
from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from schemas.design import DesignCreate, DesignUpdate, DesignResponse
from schemas.fabric import FabricCreate, FabricUpdate, FabricResponse
from schemas.color import ColorCreate, ColorUpdate, ColorResponse

__all__ = [
    "UserRegister",
    "UserLogin",
    "Token",
    "UserResponse",
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryResponse",
    "DesignCreate",
    "DesignUpdate",
    "DesignResponse",
    "FabricCreate",
    "FabricUpdate",
    "FabricResponse",
    "ColorCreate",
    "ColorUpdate",
    "ColorResponse",
]
