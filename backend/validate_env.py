#!/usr/bin/env python3
"""
Environment validation script for Tiraz Backend
Validates that all required environment variables are properly set
"""

import sys
import os
from pathlib import Path


def validate_env():
    """Validate environment variables"""
    errors = []
    warnings = []

    # Required variables
    required_vars = {
        "DATABASE_URL": "PostgreSQL database connection URL",
        "SECRET_KEY": "Secret key for JWT token signing (min 32 chars)",
    }

    # Optional variables with defaults
    optional_vars = {
        "ENVIRONMENT": "development",
        "ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
        "API_V1_PREFIX": "/api/v1",
        "CORS_ORIGINS": "http://localhost:3000,http://localhost:8080",
        "AI_SERVICE_URL": "http://ai-models:8000",
        "DEBUG": "true",
    }

    print("=" * 60)
    print("Tiraz Backend - Environment Validation")
    print("=" * 60)
    print()

    # Check required variables
    print("Checking required environment variables...")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            errors.append(f"❌ {var} is not set ({description})")
        else:
            # Validate SECRET_KEY
            if var == "SECRET_KEY":
                if len(value) < 32:
                    errors.append(f"❌ {var} must be at least 32 characters long")
                elif any(
                    weak in value.lower()
                    for weak in ["secret", "password", "change-this", "your-"]
                ):
                    warnings.append(f"⚠️  {var} appears to be a weak/default value")
                else:
                    print(f"✅ {var} is set (length: {len(value)})")

            # Validate DATABASE_URL
            elif var == "DATABASE_URL":
                if "postgresql://" in value:
                    print(f"✅ {var} is set (PostgreSQL)")
                elif "sqlite://" in value:
                    warnings.append(
                        f"⚠️  {var} is using SQLite (not recommended for production)"
                    )
                else:
                    errors.append(f"❌ {var} has invalid format")

    print()

    # Check optional variables
    print("Checking optional environment variables...")
    for var, default in optional_vars.items():
        value = os.getenv(var, default)
        print(f"  {var}={value}")

    print()
    print("=" * 60)

    # Print warnings
    if warnings:
        print()
        print("WARNINGS:")
        for warning in warnings:
            print(warning)

    # Print errors
    if errors:
        print()
        print("ERRORS:")
        for error in errors:
            print(error)
        print()
        print("❌ Environment validation FAILED")
        print()
        print("To fix:")
        print("1. Copy .env.example to .env")
        print("2. Update the values in .env with your actual configuration")
        print("3. Run this script again to validate")
        return False

    print()
    print("✅ Environment validation PASSED")
    return True


if __name__ == "__main__":
    # Load .env file if it exists
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        from dotenv import load_dotenv

        load_dotenv(env_file)
        print(f"Loaded environment from: {env_file}")
        print()

    success = validate_env()
    sys.exit(0 if success else 1)
