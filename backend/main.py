from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api.v1.api import api_router

app = FastAPI(title="Taarez Backend (FastAPI)")

# Configure CORS with settings from environment
# For GitHub Codespaces, we need to allow dynamic subdomain URLs
cors_kwargs = {
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}

# In development, allow GitHub Codespaces URLs with regex pattern
if settings.is_development:
    # Allow any *.app.github.dev subdomain for Codespaces
    cors_kwargs["allow_origin_regex"] = r"https://.*\.app\.github\.dev"
else:
    # In production, use explicit allow_origins
    cors_kwargs["allow_origins"] = settings.CORS_ORIGINS

app.add_middleware(CORSMiddleware, **cors_kwargs)

# Include API routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "service": "taarez-backend"}
