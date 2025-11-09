"""
Measurement schemas for API request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime
import uuid


class MeasurementResult(BaseModel):
    """Schema for measurement results from AI service."""

    chest: float = Field(..., description="Chest measurement in cm")
    waist: float = Field(..., description="Waist measurement in cm")
    shoulders: float = Field(..., description="Shoulder width in cm")
    arm_length: float = Field(..., description="Arm length in cm")
    neck: float = Field(..., description="Neck measurement in cm")
    hip: float = Field(..., description="Hip measurement in cm")


class MeasurementUploadResponse(BaseModel):
    """Response after uploading photos."""

    message: str
    image_paths: Dict[str, str]


class MeasurementProcessRequest(BaseModel):
    """Request schema for processing measurements."""

    height: float = Field(..., gt=0, description="Height in cm")
    weight: float = Field(..., gt=0, description="Weight in kg")


class MeasurementProcessResponse(BaseModel):
    """Response after processing measurements."""

    id: uuid.UUID
    user_id: uuid.UUID
    measurements: MeasurementResult
    confidence_score: float
    processed_at: datetime

    class Config:
        from_attributes = True


class MeasurementResponse(BaseModel):
    """Complete measurement record response."""

    id: uuid.UUID
    user_id: uuid.UUID
    measurements: Dict[str, float]
    image_paths: Dict[str, str]
    processed_at: datetime
    confidence_score: float

    class Config:
        from_attributes = True
