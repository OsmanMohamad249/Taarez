"""
API v1 router.
"""

from fastapi import APIRouter

from api.v1.endpoints import auth, users, login, measurements, categories, designs
from api.v1.endpoints import admin

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    measurements.router, prefix="/measurements", tags=["measurements"]
)
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(designs.router, prefix="/designs", tags=["designs"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
