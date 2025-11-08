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
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
