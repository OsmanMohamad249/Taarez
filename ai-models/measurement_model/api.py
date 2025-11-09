#!/usr/bin/env python3
"""
Tiraz AI Measurement Service
FastAPI API for body measurement extraction from photos
"""

from fastapi import FastAPI, APIRouter, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create router for measurement endpoints
router = APIRouter()

# Configuration
UPLOAD_FOLDER = 'data/input'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

@router.get('/health')
async def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'service': 'Tiraz AI Measurement Service',
        'version': '1.0.0'
    }

@router.post('/api/measurements/process')
async def process_measurements(
    photo_front: UploadFile = File(...),
    photo_back: UploadFile = File(...),
    photo_left: UploadFile = File(...),
    photo_right: UploadFile = File(...),
    height: float = Form(...),
    weight: float = Form(...)
):
    """
    Process body measurements from uploaded photos
    
    Expected form data:
    - photo_front: file
    - photo_back: file
    - photo_left: file
    - photo_right: file
    - height: number (cm)
    - weight: number (kg)
    """
    try:
        # Validate files are images
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
        photos = [photo_front, photo_back, photo_left, photo_right]
        
        for photo in photos:
            if photo.content_type not in allowed_types:
                raise HTTPException(
                    status_code=400,
                    detail=f'Invalid file type for {photo.filename}. Only JPEG and PNG are allowed.'
                )
        
        # Validate height and weight
        if height <= 0 or weight <= 0:
            raise HTTPException(
                status_code=400,
                detail='Height and weight must be positive numbers'
            )
        
        # TODO: Implement actual AI processing
        # For MVP, return mock measurements
        # In production, this would:
        # 1. Save uploaded photos
        # 2. Preprocess images
        # 3. Run through ML model
        # 4. Extract measurements
        # 5. Apply calibration based on height/weight
        
        measurements = {
            'chest': calculate_measurement(height, weight, 'chest'),
            'waist': calculate_measurement(height, weight, 'waist'),
            'shoulders': calculate_measurement(height, weight, 'shoulders'),
            'arm_length': calculate_measurement(height, weight, 'arm'),
            'neck': calculate_measurement(height, weight, 'neck'),
            'hip': calculate_measurement(height, weight, 'hip'),
        }
        
        return {
            'status': 'success',
            'data': {
                'measurements': measurements,
                'unit': 'cm',
                'confidence': 0.92,
                'height': height,
                'weight': weight
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        # Log error for debugging but don't expose stack trace
        print(f'Error processing measurements: {str(e)}')
        raise HTTPException(
            status_code=500,
            detail='Failed to process measurements. Please try again.'
        )

def calculate_measurement(height: float, weight: float, body_part: str) -> float:
    """
    Calculate body measurements based on height and weight
    This is a simplified algorithm for MVP
    In production, this would use the AI model
    """
    # BMI calculation
    bmi = weight / ((height / 100) ** 2)
    
    # Base measurements (for average BMI of 22)
    base_measurements = {
        'chest': height * 0.56,
        'waist': height * 0.47,
        'shoulders': height * 0.25,
        'arm': height * 0.36,
        'neck': height * 0.22,
        'hip': height * 0.55,
    }
    
    # Adjust for BMI
    bmi_factor = bmi / 22.0
    adjusted = base_measurements[body_part] * (0.85 + 0.15 * bmi_factor)
    
    return round(adjusted, 1)

@router.post('/api/measurements/validate')
async def validate_photo(photo: UploadFile = File(...)):
    """
    Validate if photo is suitable for measurement extraction
    """
    try:
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
        if photo.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail='Invalid file type. Only JPEG and PNG are allowed.'
            )
        
        # TODO: Implement photo validation
        # - Check image quality
        # - Detect if person is in frame
        # - Check pose is correct
        # - Verify lighting conditions
        
        return {
            'status': 'success',
            'data': {
                'valid': True,
                'quality_score': 0.85,
                'suggestions': []
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        # Log error for debugging but don't expose stack trace
        print(f'Error validating photo: {str(e)}')
        raise HTTPException(
            status_code=500,
            detail='Failed to validate photo. Please try again.'
        )

# Create FastAPI app and include router
app = FastAPI(title="Tiraz AI Measurement Service", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    port = int(os.getenv('PORT', 8000))
    
    print(f"🚀 Starting Tiraz AI Measurement Service on port {port}")
    
    uvicorn.run(app, host='0.0.0.0', port=port)
