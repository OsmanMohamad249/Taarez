#!/usr/bin/env python3
"""
Tiraz AI Measurement Service
Flask API for body measurement extraction from photos
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'data/input'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Tiraz AI Measurement Service',
        'version': '1.0.0'
    })

@app.route('/api/measurements/process', methods=['POST'])
def process_measurements():
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
        # Validate files
        required_photos = ['photo_front', 'photo_back', 'photo_left', 'photo_right']
        for photo_key in required_photos:
            if photo_key not in request.files:
                return jsonify({
                    'status': 'error',
                    'message': f'Missing {photo_key}'
                }), 400
        
        # Get height and weight
        height = request.form.get('height', type=float)
        weight = request.form.get('weight', type=float)
        
        if not height or not weight:
            return jsonify({
                'status': 'error',
                'message': 'Height and weight are required'
            }), 400
        
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
        
        return jsonify({
            'status': 'success',
            'data': {
                'measurements': measurements,
                'unit': 'cm',
                'confidence': 0.92,
                'height': height,
                'weight': weight
            }
        })
        
    except Exception as e:
        # Log error for debugging but don't expose stack trace
        app.logger.error(f'Error processing measurements: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Failed to process measurements. Please try again.'
        }), 500

def calculate_measurement(height, weight, body_part):
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

@app.route('/api/measurements/validate', methods=['POST'])
def validate_photo():
    """
    Validate if photo is suitable for measurement extraction
    """
    try:
        if 'photo' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No photo provided'
            }), 400
        
        # TODO: Implement photo validation
        # - Check image quality
        # - Detect if person is in frame
        # - Check pose is correct
        # - Verify lighting conditions
        
        return jsonify({
            'status': 'success',
            'data': {
                'valid': True,
                'quality_score': 0.85,
                'suggestions': []
            }
        })
        
    except Exception as e:
        # Log error for debugging but don't expose stack trace
        app.logger.error(f'Error validating photo: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Failed to validate photo. Please try again.'
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('DEBUG', 'False') == 'True'
    
    print(f"🚀 Starting Tiraz AI Measurement Service on port {port}")
    print(f"📍 Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
