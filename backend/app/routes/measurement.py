from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import os

router = APIRouter()

class ProcessRequest(BaseModel):
    height: float
    weight: float
    userId: str

@router.post("/upload")
async def upload_photos(files: List[UploadFile] = File(...), userId: str = Form(...)):
    """
    Save uploaded photos to uploads/measurements and return saved paths.
    Clients: mobile app / web frontend (multipart/form-data).
    """
    upload_dir = "uploads/measurements/"
    os.makedirs(upload_dir, exist_ok=True)
    saved = []
    for f in files:
        if f.content_type not in ("image/jpeg", "image/png"):
            raise HTTPException(status_code=400, detail="Only JPEG/PNG allowed")
        filename = f"{int(datetime.utcnow().timestamp())}-{f.filename}"
        path = os.path.join(upload_dir, filename)
        content = await f.read()
        with open(path, "wb") as fh:
            fh.write(content)
        saved.append(path)
    return {"status": "success", "files": saved, "userId": userId}

@router.post("/process")
async def process_measurements(payload: ProcessRequest):
    """
    Example endpoint that would call the AI measurement service (local or internal).
    For now returns a mocked response consistent with previous API.
    """
    mock = {
        "chest": 98,
        "waist": 82,
        "shoulders": 44,
        "armLength": 62,
        "neck": 38,
        "hip": 96,
        "height": payload.height,
        "weight": payload.weight,
        "unit": "cm",
    }
    return {
        "status": "success",
        "message": "Measurements processed successfully (mock)",
        "data": {
            "measurements": mock,
            "userId": payload.userId,
            "processedAt": datetime.utcnow().isoformat() + "Z",
        },
    }