#!/bin/bash
set -e

echo "Starting Taarez Backend..."

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application
echo "Starting FastAPI application on port 8000..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
