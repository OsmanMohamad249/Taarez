"""
Pytest configuration for backend tests.
"""
import pytest
from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv

# Load test environment variables early
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env.test'))

# Mock RateLimiter for tests - do this before importing the application
import fastapi_limiter
from fastapi_limiter.depends import RateLimiter

class MockRedis:
    async def script_load(self, script):
        return "mock_sha"

    async def evalsha(self, sha, keys, *args):
        return 0

from starlette.requests import Request
from starlette.responses import Response

class MockRateLimiter:
    def __init__(self, times=None, seconds=None):
        pass

    async def __call__(self, request: Request, response: Response):
        return None

# Initialize FastAPILimiter with mock redis before anything else
# Prepare a module-level mock redis instance (do not init FastAPILimiter here)
mock_redis = MockRedis()

# Monkey patch RateLimiter early so imports that happen later pick it up
fastapi_limiter.depends.RateLimiter = MockRateLimiter

# As a safety-net for tests, patch FastAPILimiter.__call__ to a noop when tests run
async def _fastapi_limiter_noop(self, request, response):
    return None

fastapi_limiter.FastAPILimiter.__call__ = _fastapi_limiter_noop


@pytest.fixture(scope="session")
def app():
    """
    Create a test app without FastAPILimiter to avoid event loop issues.
    """
    # Set test environment
    os.environ["TESTING"] = "true"

    # Create a new FastAPI app for testing without rate limiting
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from core.config import settings
    from api.v1.api import api_router

    test_app = FastAPI(title="Qeyafa Backend (Test)")

    # Configure CORS
    cors_origins = settings.CORS_ORIGINS  # This is a property that parses CORS_ORIGINS_STR
    cors_origins_regex = None
    if any("github.dev" in origin for origin in cors_origins):
        cors_origins_regex = r"https://.*\.app\.github\.dev"

    test_app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_origin_regex=cors_origins_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router WITHOUT rate limiting
    test_app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    # Add health endpoint
    @test_app.get("/health", tags=["health"])
    async def health():
        return {"status": "ok"}

    # Add lifespan event to initialize FastAPILimiter (even though it's mocked)
    @test_app.on_event("startup")
    async def startup_event():
        from fastapi_limiter import FastAPILimiter
        # Mock Redis client for testing
        class MockRedis:
            pass
        await FastAPILimiter.init(MockRedis())

    return test_app


@pytest.fixture(scope="function")
def client(app):
    """
    Create a test client for the app.
    """
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """
    Setup database for tests.
    """
    from core.database import Base, engine
    from core.config import settings
    from alembic.config import Config
    from alembic import command
    import os

    # Run Alembic migrations to create the test schema (use settings.DATABASE_URL)
    alembic_ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'alembic.ini'))
    alembic_cfg = Config(alembic_ini_path)
    # Run Alembic migrations to create the test schema. Do not silently
    # fall back to SQLAlchemy `create_all()` so missing migrations surface
    # and can be fixed explicitly on the branch.
    command.upgrade(alembic_cfg, "head")

    # Create test admin user
    from core.security import hash_password
    from models.user import User
    from models.roles import UserRole
    from sqlalchemy.orm import Session

    db = Session(engine)
    try:
        # Check if admin user exists
        admin_user = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin_user:
            admin_user = User(
                email="admin@example.com",
                hashed_password=hash_password("password123"),
                first_name="Admin",
                last_name="User",
                role=UserRole.ADMIN,
                is_active=True,
                is_superuser=True,
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()

    yield

    # Teardown by downgrading migrations to base. Allow errors to surface
    # to encourage fixing migration issues on the branch rather than masking them.
    command.downgrade(alembic_cfg, "base")
