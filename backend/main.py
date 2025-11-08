from fastapi import FastAPI

app = FastAPI(title="Tiraz Backend (FastAPI Boilerplate)")

@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "service": "tirez-backend"}
