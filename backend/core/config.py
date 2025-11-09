"""
Configuration settings for the application.
"""

from typing import List
from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """Application settings with environment variable validation"""

    # Environment Configuration
    ENVIRONMENT: str = Field(
        default="development",
        description="Application environment (development, staging, production)",
    )

    # Database - REQUIRED, no default for security
    DATABASE_URL: str = Field(
        ...,
        description="Database connection URL (e.g., postgresql://user:pass@host:port/db)",
    )

    # Security - REQUIRED, no default for security
    SECRET_KEY: str = Field(
        ...,
        description="Secret key for JWT token signing (must be kept secret)",
        min_length=32,
    )
    ALGORITHM: str = Field(
        default="HS256",
        description="Algorithm for JWT token encoding",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration time in minutes",
        ge=1,
    )

    # API
    API_V1_PREFIX: str = Field(
        default="/api/v1",
        description="API v1 prefix path",
    )

    # CORS Settings - More restrictive by default
    # Stored as string, accessed via property as list
    CORS_ORIGINS_STR: str = Field(
        default="http://localhost:3000,http://localhost:8080",
        description="Allowed CORS origins (comma-separated in env)",
        env="CORS_ORIGINS",
    )

    # AI Service - Optional with sensible default
    AI_SERVICE_URL: str = Field(
        default="http://ai-models:8000",
        description="AI service URL for model inference",
    )

    # Debug mode - automatically set based on environment
    DEBUG: bool = Field(
        default=True,
        description="Debug mode (automatically False in production)",
    )

    @validator("ENVIRONMENT")
    def validate_environment(cls, v):
        """Validate ENVIRONMENT is one of the allowed values"""
        allowed = ["development", "staging", "production"]
        if v.lower() not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {allowed}, got: {v}")
        return v.lower()

    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        """Validate SECRET_KEY is not a default/weak value"""
        weak_keys = [
            "your-secret-key",
            "your-secret-key-change-this-in-production",
            "change-this",
            "secret",
            "password",
        ]
        if any(weak in v.lower() for weak in weak_keys):
            raise ValueError(
                "SECRET_KEY appears to be a weak/default value. "
                "Please set a strong secret key in your environment variables."
            )
        return v

    @validator("DEBUG", pre=True, always=True, allow_reuse=True)
    def set_debug_mode(cls, v, values):
        """Automatically set DEBUG to False in production environment"""
        if "ENVIRONMENT" in values and values["ENVIRONMENT"] == "production":
            return False
        # Allow explicit override for development/staging
        return v

    @property
    def CORS_ORIGINS(self) -> List[str]:
        """Parse and return CORS origins as a list"""
        return [origin.strip() for origin in self.CORS_ORIGINS_STR.split(",")]

    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.ENVIRONMENT == "development"

    @property
    def is_staging(self) -> bool:
        """Check if running in staging mode"""
        return self.ENVIRONMENT == "staging"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.ENVIRONMENT == "production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
