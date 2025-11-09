"""
Configuration settings for the application.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://tiraz:tiraz_password@postgres:5432/tiraz_db"
    )

    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "your-secret-key-change-this-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API
    API_V1_PREFIX: str = "/api/v1"

    # AI Service
    AI_SERVICE_URL: str = os.getenv(
        "AI_SERVICE_URL", "http://ai-models:8000"  # Default internal Docker service name
    )


settings = Settings()
