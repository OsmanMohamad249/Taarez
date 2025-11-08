"""
Main entry point for Tiraz application
تطبيق طراز - Tiraz Application
"""
import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Create Flask app
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    # Note: Debug mode is enabled for development only
    # For production, set FLASK_ENV=production and use a production server like gunicorn
    debug_mode = config_name == 'development'
    
    # Get port from environment variable, default to 8080
    # Validate that PORT is a valid integer
    try:
        port = int(os.environ.get('PORT', 8080))
        if port < 1 or port > 65535:
            raise ValueError("Port must be between 1 and 65535")
    except (ValueError, TypeError) as e:
        print(f"Warning: Invalid PORT value, using default 8080. Error: {e}")
        port = 8080
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
