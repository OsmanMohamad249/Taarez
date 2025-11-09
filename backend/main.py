from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api.v1.api import api_router

app = FastAPI(title="Tiraz Backend (FastAPI)")

# Configure CORS with settings from environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "service": "tirez-backend"}
