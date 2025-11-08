from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.measurement import router as measurement_router

app = FastAPI(title="Tiraz Backend (FastAPI)", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # اضبط هذا لاحقاً للبيئة الإنتاجية
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(measurement_router, prefix="/api/v1/measurements", tags=["measurements"])

@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "service": "tiraz-backend", "timestamp": None}
