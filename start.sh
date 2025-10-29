#!/bin/bash
set -e  # Exit on error

# Production startup script
echo "Starting UnreliableUnicorn API..."

# Debug: Check DATABASE_URL (hide password)
echo "DATABASE_URL check:"
if [ -z "$DATABASE_URL" ]; then
    echo "  ERROR: DATABASE_URL is not set!"
    exit 1
else
    echo "  DATABASE_URL is set (starts with: ${DATABASE_URL:0:20}...)"
fi

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application with gunicorn
echo "Starting application with gunicorn..."
exec gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
