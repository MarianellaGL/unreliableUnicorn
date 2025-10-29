#!/bin/bash
# Production startup script

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application with gunicorn
echo "Starting application..."
gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
