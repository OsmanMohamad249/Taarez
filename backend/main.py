from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api.v1.api import api_router

app = FastAPI(title="Taarez Backend (FastAPI)")

# Configure CORS with settings from environment
# Support for GitHub Codespaces with regex patterns
cors_origins = settings.CORS_ORIGINS.copy()

# Add GitHub Codespaces pattern support
# Pattern: https://*.app.github.dev
cors_origins_regex = None
if any("github.dev" in origin for origin in cors_origins):
    # If any GitHub Codespaces URL is configured, allow all Codespaces URLs
    cors_origins_regex = r"https://.*\.app\.github\.dev"

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=cors_origins_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "service": "taarez-backend"}
