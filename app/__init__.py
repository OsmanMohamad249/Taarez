"""
Qeyafa Application Factory
تطبيق قيافة - Qeyafa Application
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app(config_name='development'):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.controllers import main_controller, item_controller
    app.register_blueprint(main_controller.bp)
    app.register_blueprint(item_controller.bp)
    
    # Register CLI commands
    from app import commands
    commands.register_commands(app)
    
    # Create or migrate database schema in non-production environments only.
    # Production schema changes must be applied via Alembic migrations.
    if config_name != 'production':
        with app.app_context():
            # Prefer running Alembic migrations if an alembic.ini is available.
            try:
                import os
                from alembic.config import Config
                from alembic import command

                # Look for alembic.ini in a couple of likely locations
                cand_paths = [
                    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'alembic.ini')),
                    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend', 'alembic.ini')),
                    os.path.abspath(os.path.join(os.getcwd(), 'alembic.ini')),
                ]
                alembic_ini = None
                for p in cand_paths:
                    if os.path.exists(p):
                        alembic_ini = p
                        break

                if alembic_ini:
                    cfg = Config(alembic_ini)
                    command.upgrade(cfg, 'head')
                else:
                    # Fail fast: do not silently fall back to SQLAlchemy create_all()
                    raise RuntimeError(
                        'alembic.ini not found; migrations must be applied via Alembic instead of create_all()'
                    )
            except Exception:
                # Surface the underlying error so it can be fixed explicitly.
                raise
    
    return app
