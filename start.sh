#!/bin/bash
set -e  # Exit on error

# Production startup script
echo "Starting UnreliableUnicorn API..."

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application with gunicorn
echo "Starting application with gunicorn..."
exec gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
