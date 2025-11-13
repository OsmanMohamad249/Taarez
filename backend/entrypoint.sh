#!/bin/bash
set -e

echo "Starting Qeyafa Backend..."

# Wait for PostgreSQL to be ready (actual DB connection)
echo "Waiting for PostgreSQL to be ready (SQLAlchemy check)..."
python wait_for_db.py "$DATABASE_URL"
echo "PostgreSQL is ready!"

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Create test users if they don't exist
echo "Creating test users (if needed)..."
python create_test_users.py || echo "Note: Test user creation had issues, continuing..."

# Start the application
echo "Starting FastAPI application on port 8000..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
